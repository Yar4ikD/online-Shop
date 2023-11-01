from django.urls import path

from .views import Payment

app_name = "api"

urlpatterns = [
    path("v1/order/pay/", Payment.as_view({"post": "update"}), name="pay_order"),
    path("v1/order/status/<int:pk>", Payment.as_view({"get": "retrieve"}), name="get_status_order"),
]
