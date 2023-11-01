from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def avatar_upload_path(instance: "Profile", filename: str) -> str:
    """Функция, указывающая путь по которому сохранять аватарки"""

    return "users/{pk}/user-details/{filename}".format(pk=instance.pk, filename=filename)


regex_phone = RegexValidator(
    regex=r"^((8|\+7|)(\d{10}))$", message=_("Формат номера телефона должен быть: +79999999999 или 89999999999")
)


class Profile(models.Model):
    """Профиль пользователя"""

    class Meta:
        ordering = ["pk"]
        verbose_name = _("профиль")
        verbose_name_plural = _("профили")

    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True, verbose_name=_("адрес"))
    phone = models.CharField(max_length=12, validators=[regex_phone], verbose_name=_("номер телефона"))
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name=_("баланс аккаунта"))
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_upload_path, verbose_name=_("аватарка"))

    def __str__(self):
        return self.user.username
