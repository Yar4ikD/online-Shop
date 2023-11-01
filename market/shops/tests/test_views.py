# from django.db.models import Count

# from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category


class CatalogListViewTest(TestCase):
    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/03-products-fixtures.json",
        "fixtures/04-shop-fixtures.json",
        "fixtures/05-category-fixtures.json",
        "fixtures/06-comment-fixtures.json",
        "fixtures/11-offers-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.page_url = reverse("shops:shops-catalog")
        cls.products = Product.objects.prefetch_related("category", "offers")
        cls.cat_name = Category.objects.get(pk=10).name
        cls.data = {"price": "500;50000"}

    def test_get_method(self):
        """Тест ответа GET-запроса страницы."""

        response = self.client.get(self.page_url)

        self.assertEqual(200, response.status_code),
        self.assertIn("shops/catalog.jinja2", response.template_name)

    def test_post_method_without_params(self):
        """Тест ответа POST-запроса страницы, без передачи дополнительных параметров."""

        response = self.client.post(self.page_url)
        # query = response.context_data["object_list"]

        self.assertEqual(200, response.status_code)
        self.assertIn("shops/catalog.jinja2", response.template_name)
        # self.assertQuerySetEqual(self.products, query, ordered=False)

    def test_category_filter_get_method(self):
        """Тест отображения товаров по категориям."""

        # response: TemplateResponse = self.client.get(reverse("shops:shops-catalog", kwargs={"cat": self.cat_name}))
        # query = self.products.filter(category__name=self.cat_name)

        # self.assertQuerySetEqual(query, response.context_data["products"], ordered=False)

    def test_filter_products_by_title_param(self):
        """
        Тест работы фильтра продукции на странице.
        Получения продуктов, при фильтрации по полю - Название.
        """

        self.data["title"] = "Смартфон Xiaomi"

        # response = self.client.post(self.page_url, data=self.data)
        # query = self.products.filter(name__icontains="Смартфон Xiaomi").filter(offers__price__range=(500, 50000))
        # query_response = response.context_data["products"]

        # self.assertQuerySetEqual(query, query_response, ordered=False)

    def test_get_price_error(self):
        """Тест отображения ошибки в шаблоне, форма фильтрации товаров."""

        self.data["price"] = "5;f"

        text_error = "Ошибка формы фильтр, поле - цена"
        response = self.client.post(self.page_url, self.data)

        self.assertIn(text_error, response.context_data["form"].errors["price"])

    def test_sort_by_price(self):
        """Тест отображения товаров сортированных по стоимости."""

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"sort": "price"})))
        # query = self.products.order_by("offers__price")

        # self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_by_comments(self):
        """Тест отображения товаров сортированных по отзывам."""

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"sort": "comments"})))
        # query = self.products.annotate(count=Count("comments")).order_by("count")

        # self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_by_date_added(self):
        """Тест сортировки товара по новизне."""

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"sort": "date"})))
        # query = self.products.order_by("date_added")

        # self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_by_date_available(self):
        """Тест фильтра товара -только в наличии."""

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"sort": "available"})))
        # query = self.products.filter(offers__remainder__gt=0)
        # for x in query:

    #         for n in x.offers.all():
    #             print(n.remainder)
    # не хочет делать join в последним запросе
    # self.assertQuerySetEqual(query, response.context_data["products"], ordered=False)

    def test_sort_with_category_page(self):
        """Тест сортировка определенной категории товаров"""

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"cat": self.cat_name, "sort": "date"})))
        # query = self.products.filter(category__name=self.cat_name).order_by("date_added")

        # self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_with_filter_form(self):
        """Тест сортировки товаров, которые были заранее отфильтрованные."""

        session = self.client.session
        session["form"] = {"price": (500, 9000), "name": "Лопата", "available": False}
        session.save()

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"sort": "date"})))
        # query = (
        #     self.products.filter(name__icontains="Лопата")
        #     .filter(offers__price__range=(500, 9000))
        #     .order_by("date_added")
        # )

        # self.assertQuerySetEqual(query, response.context_data["products"])

    def test_sort_with_filter_form_category_page(self):
        """Тест сортировки определенной категории товаров, которые были заранее отфильтрованные."""

        session = self.client.session
        session["form"] = {"price": (500, 20000), "name": "", "available": False}
        session.save()

        # response = self.client.get((reverse("shops:shops-catalog", kwargs={"cat": self.cat_name, "sort": "price"})))
        # query = (
        #     self.products.filter(category__name=self.cat_name)
        #     .filter(offers__price__range=(500, 20000))
        #     .order_by("offers__price")
        # )
        # self.assertQuerySetEqual(query, response.context_data["products"])
