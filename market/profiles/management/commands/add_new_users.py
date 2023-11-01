"""Модуль регистрации новых пользователей"""
import random
import sys
from typing import List

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import IntegrityError, transaction
from profiles.models import Profile


class Command(BaseCommand):
    """Класс реализует добавления данных в таблицу User и Profile"""

    def __init__(self):
        super(Command, self).__init__()

        self.__user_name = ["oleg", "serj", "antik", "mamon", "miha"]
        self.__password = "admin27admin"
        self.__emails = [
            "testmail1@yandex.ru",
            "mailuser@gmail.com",
            "myemail@mail.ru",
            "seller@yandex.ru",
            "profile@mail.ru",
        ]
        self.__first_name = ["Олег", "Сергей", "Антон", "Мамон", "Михалыч"]
        self.__last_name = ["Простой", "Щедрый", "Красивый", "Добрый", "Злой"]
        self.__address = [
            "Москва, ул. Большая 2",
            "Тула, ул. Серп д.34",
            "Маями, ул. Советская 2",
            "Париж, ул. Простая 143",
            "Берлин, ул. Берлин 9",
        ]

    def handle(self, *args, **options):
        sys.stdout.write("Создания профилей пользователей:\n")
        self.register_profile()

    @transaction.atomic
    def register_profile(self):
        try:
            for num in range(self.get_count):
                user = User.objects.create_user(
                    username=self.get_user_name[num], password=self.get_password
                )  # получаем User
                user.first_name = self.get_first_name[num]
                user.last_name = self.get_last_name[num]
                user.email = self.get_mail[num]
                user.save()

                profile = Profile.objects.create(
                    user=user, phone=self.get_phone, address=self.get_address[num]
                )  # создаем и получаем профиль пользователя

                sys.stdout.write(f"Успешно добавлен профиль > {profile} в БД.\n")

        except IntegrityError:
            sys.stderr.write(
                "Данная команда была использованная для этой БД.\nМожете изменить данные и запустить команду повторно."
            )

        else:
            sys.stdout.write("Команда завершила свою работу без ошибок!")

    @property
    def get_first_name(self) -> List[str]:
        return self.__first_name

    @property
    def get_last_name(self) -> List[str]:
        return self.__last_name

    @property
    def get_user_name(self) -> List[str]:
        return self.__user_name

    @property
    def get_password(self) -> str:
        return self.__password

    @property
    def get_mail(self) -> List[str]:
        return self.__emails

    @property
    def get_count(self) -> int:
        return len(self.__user_name)

    @property
    def get_phone(self) -> str:
        number = "+7"
        number += "".join([str(random.randint(0, 9)) for _ in range(10)])
        return number

    @property
    def get_address(self) -> List[str]:
        return self.__address
