from django.test import TestCase
from django.urls import reverse
from basket.models import Basket
from products.models import Product
from shops.models import Offer
from django.contrib.auth.models import User


class BasketViewTestCase(TestCase):
    """Тест представления корзины"""

    def setUp(self) -> None:
        self.get_response = self.client.get(reverse(viewname="basket:basket_view"))

    def test_url_view_exist(self):
        response = self.client.get("/ru/basket/")
        self.assertEqual(response.status_code, 200)

    def test_url_view_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, "basket/basket-view.jinja2")


class BasketAddProductTestCase(TestCase):
    """Тест добавления продукта в корзину"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/08-details-fixtures.json",
        "fixtures/09-products-detail-fixtures.json",
        "fixtures/11-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.get(pk=1)
        cls.offer = Offer.objects.get(pk=1)
        cls.user = User.objects.get(pk=2)

        cls.page_add_product_in_basket = reverse(
            viewname="basket:add_product", kwargs={"product_pk": cls.product.pk, "offer_pk": cls.offer.pk}
        )
        cls.page_add_random_product_in_basket = reverse(
            viewname="basket:add_random_product", kwargs={"product_pk": cls.product.pk}
        )

    def test_basket_added(self):
        """Тест создания корзины и ее проверка"""
        basket = Basket.objects.create(
            user=self.user,
            offer=self.offer,
            product=self.product,
            amount=1,
        )

        response = self.client.post(self.page_add_product_in_basket, data={"amount": 1})
        self.assertRedirects(response=response, expected_url=reverse(viewname="basket:basket_view"))

        self.client.post(path=reverse(viewname="profiles:login"), data={"email": "test@mail.ru", "password": "test_1"})
        self.assertEqual(basket.amount, 1)

    def test_added_random_product(self):
        """Тест на добавления продукта без выбора магазина"""
        self.client.force_login(user=self.user)
        self.client.post(
            path=self.page_add_random_product_in_basket, data={"product_pk": self.product.pk, "amount": 1}
        )
        basket = Basket.objects.filter(user=self.user)
        self.assertEqual(basket.count(), 1)

    def test_added_product(self):
        """Тест на добавления продукта с выбором магазина"""
        self.client.force_login(user=self.user)
        self.client.post(
            path=self.page_add_product_in_basket,
            data={"product_pk": self.product.pk, "offer_pk": self.offer.pk, "amount": 3},
        )
        basket = Basket.objects.get(user=self.user)
        self.assertEqual(basket.amount, 3)


class RemoveProductTestCase(TestCase):
    """Тест на удаление продукта из корзины"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/08-details-fixtures.json",
        "fixtures/09-products-detail-fixtures.json",
        "fixtures/11-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.get(pk=1)
        cls.offer = Offer.objects.get(pk=50)
        cls.user = User.objects.get(pk=2)

        cls.page_add_product_in_basket = reverse(
            viewname="basket:add_product", kwargs={"product_pk": cls.product.pk, "offer_pk": cls.offer.pk}
        )

        cls.page_remove_product_in_basket = reverse(
            viewname="basket:remove_product", kwargs={"offer_pk": cls.offer.pk}
        )

    def test_remove_product(self):
        """Тест на удаление продукта из корзины пользователя"""
        self.client.force_login(user=self.user)
        self.client.post(
            path=self.page_add_product_in_basket,
            data={"product_pk": self.product.pk, "offer_pk": self.offer.pk, "amount": 10},
        )
        basket = Basket.objects.get(user=self.user)
        self.assertEqual(basket.amount, 10)
        self.assertEqual(len(self.client.session["basket"]), 1)

        response = self.client.get(path=self.page_remove_product_in_basket, data={"offer_pk": self.offer.pk})
        self.assertRedirects(
            response=response,
            expected_url=reverse(
                viewname="basket:basket_view",
            ),
        )
        self.assertEqual(len(self.client.session["basket"]), 0)

    def test_basket_remove_product_if_not_in_basket(self):
        """Тест который выводит ошибку 404 при попытке удалить товар, которого нет в корзине у пользователя"""
        self.client.force_login(user=self.user)
        response = self.client.get(path=self.page_remove_product_in_basket, data={"offer_pk": self.offer.pk})

        self.assertEqual(response.status_code, 404)


class ChangeAmountProductTestCase(TestCase):
    """Тест для изменения количество продукта в корзине пользователя"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/08-details-fixtures.json",
        "fixtures/09-products-detail-fixtures.json",
        "fixtures/11-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.get(pk=1)
        cls.offer = Offer.objects.get(pk=1)
        cls.user = User.objects.get(pk=2)

        cls.page_add_product_in_basket = reverse(
            viewname="basket:add_product", kwargs={"product_pk": cls.product.pk, "offer_pk": cls.offer.pk}
        )

        cls.page_change_positive_ammount_product = reverse(
            viewname="basket:change_amount", kwargs={"offer_pk": cls.offer.pk, "amount": "+1"}
        )

        cls.page_change_negative_ammount_product = reverse(
            viewname="basket:change_amount", kwargs={"offer_pk": cls.offer.pk, "amount": "-1"}
        )

    def test_change_amount_product(self):
        """Тест изменяет количество продукта в корзине в положительную и отрицательную сторону"""
        self.client.force_login(user=self.user)
        self.client.post(
            path=self.page_add_product_in_basket,
            data={"product_pk": self.product.pk, "offer_pk": self.offer.pk, "amount": 5},
        )
        basket = Basket.objects.get(user=self.user)
        self.assertEqual(basket.amount, 5)

        response = self.client.get(
            reverse(
                viewname="basket:change_amount",
                kwargs={"offer_pk": self.offer.pk, "amount": "+1"},
            )
        )
        self.assertRedirects(response, expected_url=reverse("basket:basket_view"))
        self.assertEqual(self.client.session["basket"][str(self.offer.pk)]["amount"], 6)

        response = self.client.get(
            reverse(
                viewname="basket:change_amount",
                kwargs={"offer_pk": self.offer.pk, "amount": "-1"},
            )
        )
        self.assertRedirects(response, expected_url=reverse("basket:basket_view"))
        self.assertEqual(self.client.session["basket"][str(self.offer.pk)]["amount"], 5)

    def test_change_amount_product_if_not_in_basket(self):
        """Тест выдает ошибку при попытке изменить количество товара, которого нет в корзине у пользователя"""
        response = self.client.get(self.page_change_positive_ammount_product)
        self.assertEqual(response.status_code, 404)
