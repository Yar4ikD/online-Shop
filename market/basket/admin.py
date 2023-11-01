from django.contrib import admin
from .models import Basket


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "offer", "product", "amount"
    list_display_links = "pk", "user", "offer", "product", "amount"
