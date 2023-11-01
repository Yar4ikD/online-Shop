from django.test import TestCase
from django.urls import reverse
from products.models import Product, ProductDetail, Detail, Category
from history.models import BrowsingHistory
from shops.models import Offer, Shop
from comments.models import Comment
from django.contrib.auth.models import User


class ProductDetailTestCase(TestCase):
    """Тест представления детальной страницы товара"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/06-comment-fixtures.json",
        "fixtures/08-details-fixtures.json",
        "fixtures/09-products-detail-fixtures.json",
        "fixtures/11-offers-fixtures.json",
        "fixtures/12-history-products-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.get(pk=1)
        cls.offer = Offer.objects.get(pk=1)
        cls.user = User.objects.get(pk=2)
        cls.product_detail = ProductDetail.objects.get(pk=7)
        cls.detail = Detail.objects.get(pk=7)
        cls.category = Category.objects.get(pk=4)
        cls.comment = Comment.objects.get(pk=1)
        cls.shop = Shop.objects.get(pk=1)
        cls.history = BrowsingHistory.objects.get(pk=1)

    def test_product_detail(self) -> None:
        """Тест представления product-detail"""
        response = self.client.get(reverse("products:product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product-detail.jinja2")
        self.assertContains(response, self.product.pk)
        self.assertContains(response, self.offer.pk)
        self.assertContains(response, self.user.pk)
        self.assertContains(response, self.product_detail.pk)
        self.assertContains(response, self.detail.pk)
        self.assertContains(response, self.category.pk)
        self.assertContains(response, self.comment.pk)
        self.assertContains(response, self.history.pk)
        self.assertFalse(response.context_data["form"].is_valid())
