"""Модуль для настройки аутентификации пользователя"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """Класс для установки аутентификации пользователя с помощью email."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)

        except user_model.DoesNotExist:
            return None

        else:
            if user.check_password(password):
                return user

        return None
