import os
import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    description = models.CharField(max_length=512, verbose_name=_("описание"))
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("категория")
        verbose_name_plural = _("категории")

    def __str__(self) -> str:
        return f"Category(pk={self.pk}, name={self.name!r})"


class Product(models.Model):
    """Модель продукт"""

    class Meta:
        verbose_name = _("продукт")
        verbose_name_plural = _("продукты")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))
    details = models.ManyToManyField("Detail", through="ProductDetail", verbose_name=_("характеристики"))
    description = models.CharField(max_length=512, verbose_name=_("описание"))
    preview = models.ImageField(blank=True, upload_to="products/preview")
    image = models.ImageField(blank=True, upload_to="products/image")
    date_added = models.DateTimeField(auto_now=True, verbose_name=_("дата добавления"))
    category = models.ForeignKey(
        Category, verbose_name=_("категория"), related_name="products", on_delete=models.PROTECT
    )
    limited = models.BooleanField(default=False, verbose_name=_("ограниченный тираж"))

    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk})


class Detail(models.Model):
    """Свойство продукта"""

    class Meta:
        verbose_name = _("характеристика")
        verbose_name_plural = _("характеристики")

    name = models.CharField(max_length=512, verbose_name=_("наименование"))

    def __str__(self) -> str:
        return f"Detail(pk={self.pk}, name={self.name!r})"


class ProductImage(models.Model):
    """Дополнительные изображения продукта"""

    class Meta:
        verbose_name = _("изображение продукта")
        verbose_name_plural = _("изображения продукта")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    image = models.ImageField(upload_to="products/image")

    def __str__(self) -> str:
        return f"ProductImage(pk={self.pk})"


class ProductDetail(models.Model):
    """Значение свойства продукта"""

    class Meta:
        verbose_name = _("свойство продукта")
        verbose_name_plural = _("свойства продукта")

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT)
    value = models.CharField(max_length=128, verbose_name=_("значение"))
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


def generate_unique_filename(instance: "UploadedFile", filename: str) -> str:
    """
    Генерация уникального имени для файла,
    чтобы после импорта он не потерялся (если файл уже есть)

    :param instance: Экземпляр модели 'UploadedFile', для которого генерируется имя файла.
    :param filename: Имя файла при загрузке
    :return: Уникальное имя файла
    """
    name_list = filename.split(".")
    ext = name_list[1]
    filename = name_list[0]
    unique_filename = f"{filename}_{str(uuid.uuid4())[:5]}.{ext}"
    return os.path.join("import_files", unique_filename)


class UploadedFile(models.Model):
    """
    Модель загрузки файла
    """

    file = models.FileField(upload_to=generate_unique_filename)

    def __str__(self):
        return self.file.name
