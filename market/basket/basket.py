from discounts.calculate import DiscountCalculation
from shops.models import Offer
from .models import Basket
from django.http import HttpRequest, Http404
from django.conf import settings
from django.shortcuts import get_object_or_404
from decimal import Decimal
import random


class BasketObject:
    """Инициализируем работу корзины для добавления товаров"""

    def __init__(self, request: HttpRequest) -> None:
        """
        Инициализация корзины в сессии
        :param: request - WSGI request
        :return: None
        """
        self.session = request.session
        self.user = request.user
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.get_basket_for_user() if self.user.is_authenticated else {}
            self.session[settings.BASKET_SESSION_ID] = basket
        self.basket = basket

    def __iter__(self) -> dict:
        """
        Метод для перебора элементов в корзине
        """
        offers_pk = [key for key in self.basket.keys()]
        offers = Offer.objects.prefetch_related("product").filter(pk__in=offers_pk)
        basket = self.basket.copy()
        for offer in offers:
            basket[str(offer.pk)]["product"] = offer.product
            basket[str(offer.pk)]["offer_pk"] = offer.pk
        for item in basket.values():
            yield item

    def get_basket_for_user(self) -> dict:
        """
        Метод для получения корзины для аутентифицированного пользователя из базы данных
        :return: словарь с данными корзины конкретного пользователя из базы данных
        """
        basket = {}
        users_basket = Basket.objects.filter(user=self.user).prefetch_related("offer")
        for user_basket in users_basket:
            basket[str(user_basket.offer.pk)] = {
                "product": user_basket.offer.product.pk,
                "amount": user_basket.amount,
                "price": str(user_basket.offer.price),
            }
        return basket

    def add_product_in_basket(self, product_pk: int, offer_pk: int, amount: int) -> None:
        """
        Метод для добавления продукта в корзину
        :param: product_pk - первичный ключ продукта
        :param: offer_pk - первичный ключ предложения
        :param: amount - количество продуктов, желаемых для добавления в корзину
        :return: None
        """
        if offer_pk is None:
            offers_ids = Offer.objects.filter(product_id=product_pk)
            offer_pk = random.choice([o_i.pk for o_i in offers_ids])
        if str(offer_pk) in self.basket:
            self.update_product_in_basket(offer_pk=offer_pk, amount=amount)
        else:
            self.add_new_product_in_basket(offer_pk=offer_pk, amount=amount)

    def add_new_product_in_basket(self, offer_pk: int, amount: int) -> None:
        """
        Метод для добавления нового продукта в корзину
        :param: offer_pk - первичный ключ предложения
        :param: amount - количество продуктов, желаемых для добавления в корзину
        :return: None
        """
        offer = Offer.objects.get(pk=offer_pk)

        discounts = DiscountCalculation(offer)
        price = discounts.get_best_discount()

        self.basket[str(offer_pk)] = {"product": offer.product.pk, "amount": amount, "price": str(price)}
        self.save()
        self.update_or_create_basket(offer_pk=offer_pk, amount=amount)

    def update_product_in_basket(self, offer_pk: int, amount) -> None:
        """
        Метод для обновления полей продукта в корзине или создания нового продукта в ней
        :param: offer_pk - первичный ключ предложения
        :param: amount - количество продуктов, желаемых для добавления в корзину
        :return: None
        """
        if str(offer_pk) in self.basket:
            self.basket[str(offer_pk)]["amount"] += amount
            if self.basket[str(offer_pk)]["amount"] <= 0:
                self.remove_product(offer_pk=offer_pk)
                self.save()
                return
            self.save()
            self.update_or_create_basket(offer_pk=offer_pk, amount=self.basket[str(offer_pk)]["amount"])
        else:
            raise Http404

    def update_or_create_basket(self, offer_pk: int, amount: int):
        """
        Метод для обновления полей или создания нового продукта в корзине
        :param: offer_pk - первичный ключ предложения
        :param: amount - количество продуктов, желаемых для добавления в корзину
        :return: None
        """
        if self.user.is_authenticated:
            offer = Offer.objects.prefetch_related("product").get(pk=offer_pk)
            obj, created = Basket.objects.update_or_create(
                offer=offer,
                defaults={
                    "user": self.user,
                    "offer": offer,
                    "product": offer.product,
                    "amount": amount,
                },
            )

    def remove_product(self, offer_pk: int) -> None:
        """
        Метод для удаления продукта из корзины
        :param: offer_pk - первичный ключ предложения
        :return: None
        """
        if str(offer_pk) in self.basket:
            del self.basket[str(offer_pk)]
            self.save()
            if self.user.is_authenticated:
                users_basket = get_object_or_404(klass=Basket, user=self.user, offer=offer_pk)
                users_basket.delete()
        else:
            raise Http404

    def get_total_price(self) -> Decimal:
        """
        Подсчет стоимости всех продуктов в корзине
        :return: сумма цен всех товаров в корзине
        """
        price = sum([Decimal(item["price"]) * item["amount"] for item in self.basket.values()])
        price = DiscountCalculation.return_basket_discount(price=price, basket_values=self.basket.values())

        return price

    def clear(self) -> None:
        """
        Удаление корзины из сессии и БД
        :return: None
        """

        del self.session[settings.BASKET_SESSION_ID]
        Basket.objects.filter(user=self.user).delete()
        self.session.modified = True

    def save(self) -> None:
        """
        Метод для сохранения корзины в сессии
        :return: None
        """
        self.session[settings.BASKET_SESSION_ID] = self.basket
        self.session.modified = True
