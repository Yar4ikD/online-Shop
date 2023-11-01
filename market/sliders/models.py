from django.db import models
from django.utils.translation import gettext_lazy as _
from products.models import Product, Category


def slider_upload_path(instance: "Slider", filename: str) -> str:
    return "sliders/image/{instance_name}_{filename}".format(instance_name=instance.title, filename=filename)


def banner_upload_path(instance: "Banner", filename: str) -> str:
    return "banners/image/{instance_name}_{filename}".format(instance_name=instance.title, filename=filename)


class Slider(models.Model):
    """Модель слайдер"""

    class Meta:
        verbose_name = _("слайдер")
        verbose_name_plural = _("слайдеры")

    title = models.CharField(max_length=200, verbose_name=_("заголовок"))
    description = models.CharField(max_length=400, verbose_name=_("описание"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sliders", verbose_name=_("продукт"))
    image = models.ImageField(upload_to=slider_upload_path, verbose_name=_("изображение слайдера"))

    def __str__(self):
        return f"Слайдер: {self.title}"


class Banner(models.Model):
    """Модель баннера главной страницы."""

    class Meta:
        verbose_name = _("баннер")
        verbose_name_plural = _("баннера")

    title = models.CharField(max_length=200, verbose_name=_("название категории товаров"))
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="banners", verbose_name=_("категория")
    )
    image = models.ImageField(upload_to=banner_upload_path, verbose_name=_("изображение баннера"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("цена от"))

    def __str__(self) -> str:
        return f"Banner - {self.title}"
