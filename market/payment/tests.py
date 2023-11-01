from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from order.models import Order, OrderStatus, Delivery
from rest_framework.test import APITestCase


class PaymentAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Создание тестового заказа
        :return: None
        """
        cls.superuser = User.objects.create_superuser(
            username="superuser", password="testpassword", email="superuser@test.com"
        )

        cls.order_status = OrderStatus.objects.create(name="создан")
        cls.delivery = Delivery.objects.create(
            delivery_type="Обычная доставка",
            city="Пермь",
            address="ул. Емельянова, д.99, кв.54",
            pay="Онлайн со случайного счета",
        )

        cls.order = Order.objects.create(
            user_id=cls.superuser.pk,
            customer="Test Customer",
            email="test@example.com",
            phone="1234567890",
            order_status_id=cls.order_status.pk,
            delivery_id=cls.delivery.pk,
            is_paid=False,
        )

    def test_get_order_status(self) -> None:
        """
        Тестирование статуса заказа, который существует в БД

        :return: None
        """
        url = reverse("api:get_status_order", kwargs={"pk": self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": self.order.pk, "status": "Не оплачен"})

    def test_get_order_status_not_exist(self) -> None:
        """
        Тестирование статуса заказа, который не существует в БД

        :return: None
        """
        url = reverse("api:get_status_order", kwargs={"pk": 50})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pay_order_not_exist(self) -> None:
        """
        Тестирование оплаты заказа, который еще не существует в БД

        :return: None
        """
        url = reverse("api:pay_order")
        data = {"order": 50, "account": "12345678", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Заказ не существует или уже оплачен")

    def test_pay_order_success(self) -> None:
        """
        Тестирование успешной оплаты заказа

        :return: None
        """
        url = reverse("api:pay_order")
        data = {"order": self.order.pk, "account": "12345678", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Оплата прошла успешно")

    def test_pay_order_with_invalid_account(self) -> None:
        """
        Тестирование оплаты заказа с некорректно введеным номером карты/счета

        :return: None
        """
        url = reverse("api:pay_order")
        data = {"order": self.order.pk, "account": "12345670", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Оплата не прошла")

        data = {"order": self.order.pk, "account": "12345671", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Оплата не прошла")

        data = {"order": self.order.pk, "account": "1234", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Оплата не прошла")

    def test_update_payment_already_paid(self) -> None:
        """
        Тестирование оплаты заказа, которая ранее уже была успешно оплачена

        :return: None
        """
        self.order.is_paid = True
        self.order.save()
        url = reverse("api:pay_order")
        data = {"order": self.order.pk, "account": "12345678", "amount": 100.00}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Заказ не существует или уже оплачен")
