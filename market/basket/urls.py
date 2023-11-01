from django.urls import path
from .views import BasketView, add_product, remove_product, change_amount_for_product_in_basket


app_name = "basket"

urlpatterns = [
    path("", BasketView.as_view(), name="basket_view"),
    path("add_product/<int:product_pk>", add_product, name="add_random_product"),
    path("add_product/<int:product_pk>/<int:offer_pk>", add_product, name="add_product"),
    path("remove/<int:offer_pk>", remove_product, name="remove_product"),
    path("change_amount/<int:offer_pk>/<str:amount>", change_amount_for_product_in_basket, name="change_amount"),
]
