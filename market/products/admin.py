from django.contrib import admin

from .models import Category, Product, Detail, ProductDetail, ProductImage


class DetailsInline(admin.TabularInline):
    model = Product.details.through


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductInline, DetailsInline]
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "detail", "value"
    list_display_links = "pk", "product"
