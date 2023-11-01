from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import RegexValidator


class Order(models.Model):
    """Модель заказа"""

    regex_phone = RegexValidator(
        regex=r"^((8|\+7|)(\d{10}))$", message=_("Формат номера телефона должен быть: +79999999999 или 89999999999")
    )

    class Meta:
        verbose_name = _("заказ")
        verbose_name_plural = _("заказы")

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("пользователь"), related_name="orders")
    customer = models.CharField(max_length=52, verbose_name=_("ФИО заказчика"))
    date_added = models.DateTimeField(auto_now=True, verbose_name=_("дата добавления"))
    email = models.EmailField(verbose_name=_("email"))
    phone = models.CharField(max_length=12, validators=[regex_phone], verbose_name=_("номер телефона"))
    products = models.ManyToManyField(
        Product, verbose_name=_("продукты в заказе"), through="ProductInOrder", related_name="orders"
    )
    order_status = models.ForeignKey("OrderStatus", verbose_name=_("статус заказа"), on_delete=models.CASCADE)
    delivery = models.ForeignKey("Delivery", verbose_name=_("доставка"), on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False, verbose_name=_("Не оплачен"))


class OrderStatus(models.Model):
    """Модель статуса заказа"""

    class Meta:
        verbose_name = _("статус заказа")
        verbose_name_plural = _("статусы заказов")

    name = models.CharField(max_length=15, verbose_name=_("название статуса"))


class DeliveryTypesChoices(models.TextChoices):
    """
    Модель для выбора типа доставки
    """

    REGULAR = "Обычная доставка", "Обычная доставка"
    EXPRESS = "Экспресс доставка", "Экспресс доставка"


class PayChoices(models.TextChoices):
    """
    Модель для выбора типа оплаты
    """

    CARD = _("Онлайн картой"), _("Онлайн картой")
    ACCOUNT = _("Онлайн со случайного счета"), _("Онлайн со случайного счета")


class Delivery(models.Model):
    """Модель доставки заказа"""

    class Meta:
        verbose_name = _("доставка заказа")
        verbose_name_plural = _("доставки заказов")

    delivery_type = models.CharField(
        max_length=512,
        default=DeliveryTypesChoices.REGULAR,
        choices=DeliveryTypesChoices.choices,
        verbose_name=_("тип доставки"),
    )
    city = models.CharField(null=True, blank=True, max_length=30, verbose_name=_("город доставки"))
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name=_("адрес доставки"))
    pay = models.CharField(
        max_length=512,
        choices=PayChoices.choices,
        default=PayChoices.CARD,
        verbose_name=_("тип оплаты"),
    )


class ProductInOrder(models.Model):
    """Модель продуктов в заказе"""

    class Meta:
        verbose_name = _("продукт в заказе")
        verbose_name_plural = _("продукты в заказе")

    product = models.ForeignKey(Product, verbose_name=_("продукт в заказе"), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name=_("заказ"), on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена"))
    amount = models.PositiveIntegerField(verbose_name=_("количество"), default=1)
