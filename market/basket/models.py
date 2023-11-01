from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product
from shops.models import Offer
from django.contrib.auth.models import User


class Basket(models.Model):
    """Корзина"""

    class Meta:
        verbose_name = _("корзина пользователя")

    user = models.ForeignKey(
        User,
        related_name="baskets",
        verbose_name=_("пользователь корзины"),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    offer = models.ForeignKey(
        Offer, related_name="baskets", verbose_name=_("предложения магазинов"), null=True, on_delete=models.PROTECT
    )

    product = models.ForeignKey(
        Product, related_name="baskets", verbose_name=_("продукт магазина"), null=True, on_delete=models.PROTECT
    )

    amount = models.PositiveIntegerField(verbose_name=_("количество"), default=1)
