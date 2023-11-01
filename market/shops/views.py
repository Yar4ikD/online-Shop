import datetime
import random

from django.core.cache import cache
from django.db.models import QuerySet, Count
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from products.models import Product
from shops.forms import CatalogFiltersForm
from django.shortcuts import render  # noqa F401

from .models import Shop, LimitedOffer


class MainPageView(ListView):
    """Класс представления главной страницы"""

    template_name = "main/index.jinja2"
    context_object_name = "products"

    def get_queryset(self):
        products = Product.objects.prefetch_related("category", "offers")[2:5]  # ПОПУЛЯРНЫЕ ТОВАРЫ - заглушка
        return products

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        limited_products = Product.objects.filter(limited=True)

        if limited_products:
            offers_time = datetime.datetime.today() + datetime.timedelta(days=1)

            context["offers_time"] = offers_time.strftime("%d.%m.%Y %H:%M:%S")
            context["limited_offers"] = limited_products

            limited_offer = cache.get("limited_offer")
            if not limited_offer:
                limited_offer = random.choice(LimitedOffer.objects.prefetch_related("product"))
                cache.set("limited_offer", limited_offer, 86400)

            context["limited_offer"] = limited_offer

        return context


class CatalogListView(FormMixin, ListView):
    """Класс представления каталога товаров"""

    form_class = CatalogFiltersForm
    template_name = "shops/catalog.jinja2"
    context_object_name = "products"
    paginate_by = 3

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get("cat", None):
            context["cat"] = self.kwargs["cat"]

        return context

    def get_queryset(self):
        product = Product.objects.prefetch_related("category", "offers")

        if self.kwargs.get("cat", None) and self.request.method == "GET":
            product = product.filter(category__name=self.kwargs["cat"])
            # self.request.session["form"] = None

        if self.kwargs.get("sort", None):  # сортировка товара
            if self.request.session.get("form", None):  # если ранее фильтрация была определена
                product = self.filter_products(products=product, filter_data=self.request.session["form"])
            product = self.sort_products(products=product, key=self.kwargs["sort"])

        if self.request.method == "POST":  # фильтрация товаров
            form = CatalogFiltersForm(self.request.POST)

            if form.is_valid():
                data = {
                    "price": form.cleaned_data.get("price"),
                    "name": form.cleaned_data.get("title", ""),
                    "available": form.cleaned_data.get("available", None),
                }
                product = self.filter_products(products=product, filter_data=data)

                if self.kwargs.get("cat", None):  # возвращаем товары по категориям
                    product = product.filter(category__name=self.kwargs["cat"])

                if self.kwargs.get("sort", None):  # сортировка товарок
                    product = self.sort_products(products=product, key=self.kwargs["sort"])

        return product

    def sort_products(self, products: QuerySet, key: str) -> QuerySet:
        """Метод сортировки товаров по заданному ключу"""

        if key == "price":
            return products.order_by("offers__price")

        if key == "comments":
            return products.annotate(count=Count("comments")).order_by("count")

        if key == "date":
            return products.order_by("date_added")

        if key == "popular":
            pass

        return products

    def filter_products(self, products: QuerySet, filter_data: dict) -> QuerySet:
        """Метод фильтрации товаров по ключам переданных из формы."""

        price_from, price_to = filter_data.get("price")
        name = filter_data.get("name")

        product = products.filter(offers__price__range=(price_from, price_to)).filter(name__icontains=name)

        if filter_data.get("available"):
            product = products.filter(offers__remainder__gt=0)

        self.request.session.set_expiry(300)
        self.request.session["form"] = filter_data  # добавляем ключи фильтрации в сессию
        return product


class ShopDetailView(DetailView):
    """View детального представления магазина"""

    context_object_name = "shop"
    template_name = "shops/shop_detail.jinja2"
    model = Shop
