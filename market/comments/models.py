from django.contrib.auth.models import User
from django.db import models
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Comment(models.Model):
    """
    Модель отзыва о продукте.
    В модели прописано 2 дополнительных метода,
    которые возвращают статистические данные.
    """

    class Meta:
        ordering = ["date_publish"]
        verbose_name = _("отзыв")
        verbose_name_plural = _("отзывы")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name=_("пользователь"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments", verbose_name=_("продукт"))
    text = models.TextField(max_length=600, blank=True, verbose_name=_("текст отзыва"))
    date_publish = models.DateTimeField(auto_now=True, verbose_name=_("дата публикации"))

    def __str__(self) -> str:
        return f"Отзыв {self.author.username} о продукте {self.product.name}"
