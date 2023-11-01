from django.contrib import admin  # noqa F401
from .models import Shop, Offer, LimitedOffer


class ProductInline(admin.TabularInline):
    model = Shop.products.through


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = "pk", "shop", "product", "price"
    list_display_links = "pk", "shop"


class LimitedOfferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "new_price",
        "old_price",
    )
    list_filter = (
        "id",
        "new_price",
    )


admin.site.register(LimitedOffer, LimitedOfferAdmin)
