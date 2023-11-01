from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag(name="sum_price")
def sum_price(basket):
    """
    Пользовательский тег возвращающий сумму цен товаров в корзине
    :param basket: Корзина пользователся в сессии
    """
    try:
        summ_price = sum([Decimal(item["price"]) * item["amount"] for item in basket.values()])
        return summ_price if summ_price > 0 else 0
    except AttributeError:
        return 0


@register.simple_tag(name="sum_amount")
def sum_amount(basket):
    """
    Пользовательский тег возвращающий сумму товаров в корзине
    :param basket: Корзина пользователся в сессии
    """
    try:
        summ_amount = sum([item["amount"] for item in basket.values()])
        return summ_amount if summ_amount > 0 else 0
    except AttributeError:
        return 0
