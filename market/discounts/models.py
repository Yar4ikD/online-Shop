from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product, Category
from shops.models import Offer


class Promotion(models.Model):
    """Базовая модель скидки, от которой наследуют все остальные модели скидок."""

    class Meta:
        abstract = True

    title = models.CharField(max_length=150, verbose_name=_("название"))
    description = models.CharField(max_length=350, verbose_name=_("описание"))
    date_start = models.DateTimeField(auto_now=True, verbose_name=_("дата начала"))
    date_finish = models.DateTimeField(verbose_name=_("дата окончания"))
    active = models.BooleanField(default=False, verbose_name=_("активный статус"))
    priority = models.IntegerField(default=1, verbose_name=_("приоритет скидки"))


class ProductDiscount(Promotion):
    """Модель скидка на товар или группу товаров."""

    class Meta:
        verbose_name = _("скидка на товары")
        verbose_name_plural = _("скидки на товары")

    product = models.ManyToManyField(Product, related_name="product_discounts", verbose_name=_("продукт"))
    percent = models.IntegerField(default=0, verbose_name=_("процент скидки"))

    def __str__(self) -> str:
        return f"Скидка на товары: {self.title}"


class CategoryDiscount(Promotion):
    """Модель скидка на категорию товаров."""

    class Meta:
        verbose_name = _("скидка на категорию товаров")
        verbose_name_plural = _("скидки на категории товаров")

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_discounts", verbose_name=_("категория товаров")
    )
    percent = models.IntegerField(default=0, verbose_name=_("процент скидки"))

    def __str__(self) -> str:
        return f"Скидка на категорию товара: {self.title}"


class BasketDiscount(Promotion):
    """Модель скидка на корзину."""

    class Meta:
        verbose_name = _("скидка на корзину")
        verbose_name_plural = _("скидки на корзину")

    offer = models.ManyToManyField(Offer, related_name="basket_discounts", verbose_name=_("предложение"))
    amount_money = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("сумма денег"))
    discount_amount = models.IntegerField(default=0, verbose_name=_("сумма скидки"))

    def __str__(self) -> str:
        return f"Скидка на корзину: {self.title}"
