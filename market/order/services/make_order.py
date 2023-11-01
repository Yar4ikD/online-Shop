from django.http import HttpRequest
from django.conf import settings
from basket.basket import BasketObject
from shops.models import Offer
from profiles.models import Profile
from decimal import Decimal
from order.models import Order, Delivery, ProductInOrder
from django.db import transaction
from django.utils.translation import gettext_lazy as _


class MakeOrder:
    """Инициализируем работу класса для создания заказа"""

    def __init__(self, request: HttpRequest):
        self.request = request
        self.user = request.user
        self.session = request.session
        order = self.session.get(settings.ORDER_SESSION_ID)
        if not order:
            order = {}
            self.session[settings.ORDER_SESSION_ID] = order
        self.order = order

    def __iter__(self):
        """
        Метод для перебора элементов в сессии заказа
        """
        order = self.order.copy()
        for item in order.values():
            yield item

    def writing_data_order_in_session(self, key: str, cleaned_data: dict) -> None:
        """
        Метод для сохранения данных заказа из форм в сессию
        :param key: ступень оформления заказа
        :param cleaned_data: данные из формы
        :return: None
        """

        self.order[key] = cleaned_data
        self.save()

    def cheking_func(self) -> bool or str:
        """
        Метод для запуска проверок данных для корректного создания заказа
        :return: False если ошибок нет, str - текст ошибки
        """
        if self.check_form_data():
            if self.check_profile_balance():
                if self.check_remainder_product():
                    self.save_order()
                    self.deleting_basket_and_order()
                    return False
                else:
                    return "В магазине недостаочное количество продукта. Приносим свои извинения."
            else:
                return "На вашем балансе недостаточно средств!"
        else:
            return "Получено недостаточно данных для оформления заказа!"

    def check_form_data(self) -> bool:
        """
        Метод для проверки наличия данных из всех форм в сессии
        :return: True еслии данные все, False если данные переданы не в полном обьеме
        """
        if "step_1" in self.order and "step_2" in self.order and "step_3" in self.order:
            return True
        return False

    def check_profile_balance(self) -> bool:
        """
        Метод для проверки баланса профиля пользователя
        :return: False если средств на балансе для оформления заказа недостаточно, True если средств хватает
        """
        users_basket = BasketObject(request=self.request)
        profile = Profile.objects.get(user=self.user)
        if users_basket.get_total_price() > profile.balance:
            return False
        return True

    def check_remainder_product(self) -> bool:
        """
        Метод для проверки количества товара в магазине
        :return: False если товара в магазине недостаточно, True если количество товара хватает
        """
        offers_pk = self.session[settings.BASKET_SESSION_ID].keys()
        basket = self.session[settings.BASKET_SESSION_ID]
        for pk in offers_pk:
            offer = Offer.objects.get(pk=pk)
            if basket[pk]["amount"] > offer.remainder:
                return False
        return True

    @transaction.atomic
    def save_order(self) -> None:
        """
        Метод для сохранения данных заказа в БД
        :return: None
        """
        basket = BasketObject(request=self.request)

        delivery = Delivery.objects.create(
            delivery_type=self.order["step_2"]["delivery_type"],
            city=self.order["step_2"]["city"],
            address=self.order["step_2"]["address"],
            pay=self.order["step_3"]["pay"],
        )
        order = Order.objects.create(
            user=self.user,
            customer=self.order["step_1"]["customer"],
            email=self.order["step_1"]["email"],
            phone=self.order["step_1"]["phone"],
            order_status_id=1,
            delivery=delivery,
        )
        for item in basket:
            price = Decimal(item["price"]) * item["amount"]
            if self.order["step_2"]["delivery_type"] == _("Экспресс доставка"):
                price += price / 100 * 5
            ProductInOrder.objects.create(product=item["product"], price=price, amount=item["amount"], order=order)

    def deleting_basket_and_order(self) -> None:
        """
        Метод для удаления корзины из сессии и БД, удаление данных заказа из сессии
        :return: None
        """
        basket = BasketObject(request=self.request)
        basket.clear()
        del self.session[settings.ORDER_SESSION_ID]
        self.session.modified = True

    def save(self) -> None:
        """
        Метод для обновления сессия заказа
        :return: None
        """
        self.session[settings.ORDER_SESSION_ID] = self.order
        self.session.modified = True
