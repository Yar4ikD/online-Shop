"""
В скрипте прописан класс для работы с таблицами скидок.
Прописана логика получения скидок на продукт, категорию или корзину.
"""
from decimal import Decimal

from discounts.models import CategoryDiscount, ProductDiscount, BasketDiscount
from django.db.models import QuerySet, Max
from shops.models import Offer


class DiscountCalculation:
    """
    Класс для получения скидки на продукт, категорию, корзину.
    """

    def __init__(self, offer: Offer) -> None:
        self.offer = offer
        self.price = offer.price
        self.product_discount = None
        self.category_discount = None

    def get_best_discount(self):
        """
        Метод класса вычисляет и возвращает найболее лучшую скидку для клиента.
        Выбирается скидка при которой ценна товара для клиента будет дешевле.
        """

        self.calculate_product_discount()
        self.calculate_category_discount()

        return self.category_discount if self.product_discount >= self.category_discount else self.product_discount

    @classmethod
    def return_basket_discount(cls, price, basket_values) -> Decimal:
        """
        Метод класса возвращает конечную цену товаров в корзине со скидкой.
        Применяются скидки только на корзину.
        """

        try:
            list_offers_pk = [item["offer_pk"] for item in basket_values]

        except KeyError:
            return price

        discounts_list = (
            BasketDiscount.objects.prefetch_related("offer").filter(active=True).filter(offer__pk__in=list_offers_pk)
        )

        if len(discounts_list) > 0:
            max_priority = discounts_list.aggregate(Max("priority"))
            discount = discounts_list.filter(priority=max_priority["priority__max"])

            if discount[0].amount_money <= price:
                price = price - discount[0].discount_amount

        return price

    def calculate_product_discount(self):
        """
        Метод расчета конечной цены товара со скидкой.
        Если к товару применяется несколько кидок,
        выбирается скидка в которой больше процент на скидку.
        """

        if ProductDiscount.objects.filter(product=self.offer.product).filter(active=True):
            product_discount = ProductDiscount.objects.filter(product=self.offer.product).filter(active=True)
            percent = self.sort_discounts(product_discount)
            self.product_discount = self.calculate_discount(self.price, percent)

        else:
            self.product_discount = self.price

    def calculate_category_discount(self):
        """
        Метод расчета конечной цены товара со скидкой на категории.
        Если к товару применяется несколько кидок,
        выбирается скидка в которой больше процент на скидку.
        """

        if CategoryDiscount.objects.filter(category=self.offer.product.category).filter(active=True):
            category_discount = CategoryDiscount.objects.filter(category=self.offer.product.category).filter(
                active=True
            )
            percent = self.sort_discounts(category_discount)
            self.category_discount = self.calculate_discount(self.price, percent)

        else:
            self.category_discount = self.price

    @classmethod
    def sort_discounts(cls, query: QuerySet) -> int:
        """
        Метод класса для сортировки списка скидок.
        Возвращает самый большой процент скидки.
        """

        sort_discount = sorted(query, key=lambda x: x.percent, reverse=True)
        return sort_discount[0].percent

    @classmethod
    def calculate_discount(cls, price, percent) -> Decimal:
        """
        Метод класса для расчета скидки для товара.
        Возвращает цену товара с учетом скидки.
        """

        discount = price * percent / 100
        price = price - discount

        return 0 if price < 0 else price
