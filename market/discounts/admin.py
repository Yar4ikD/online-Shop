from discounts.models import ProductDiscount, CategoryDiscount, BasketDiscount
from django.contrib import admin
from shops.models import Offer


class DetailsInline(admin.TabularInline):
    model = Offer.basket_discounts.through


class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date_start",
        "active",
        "priority",
    )
    list_filter = (
        "id",
        "title",
        "date_start",
        "active",
        "priority",
    )
    list_display_links = ("title",)
    search_fields = ("title",)


class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "date_start",
        "active",
        "priority",
    )
    list_filter = (
        "id",
        "title",
        "date_start",
        "active",
        "priority",
    )
    list_display_links = ("title",)
    search_fields = ("title",)


class BasketDiscountAdmin(admin.ModelAdmin):
    inlines = [DetailsInline]
    list_display = (
        "id",
        "title",
        "date_start",
        "active",
        "priority",
    )
    list_filter = (
        "id",
        "date_start",
        "active",
        "priority",
    )
    list_display_links = ("title",)
    search_fields = ("title",)


admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(CategoryDiscount, CategoryDiscountAdmin)
admin.site.register(BasketDiscount, BasketDiscountAdmin)
