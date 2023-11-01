from discounts.views import DiscountsListView
from django.urls import path

app_name = "discount"

urlpatterns = [
    path("", DiscountsListView.as_view(), name="registration_user"),
]
