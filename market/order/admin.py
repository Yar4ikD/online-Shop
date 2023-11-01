from django.contrib import admin
from order.models import Order, Delivery, OrderStatus, ProductInOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "customer", "date_added", "email", "phone", "order_status", "delivery"
    list_display_links = "pk", "user", "customer", "date_added", "email", "phone", "order_status", "delivery"


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = "pk", "delivery_type", "city", "address", "pay"
    list_display_links = "pk", "delivery_type", "city", "address", "pay"


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = "pk", "product", "order", "price", "amount"
    list_display_links = "pk", "product", "order", "price", "amount"
