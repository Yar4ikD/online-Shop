from django.urls import path
from .views import ShopDetailView, CatalogListView, MainPageView

app_name = "shops"

urlpatterns = [
    path("", MainPageView.as_view(), name="main-page"),
    path("catalog/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/<str:cat>/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/sort/<str:sort>/", CatalogListView.as_view(), name="shops-catalog"),
    path("catalog/<str:cat>/sort/<str:sort>/", CatalogListView.as_view(), name="shops-catalog"),
    path("<int:pk>/", ShopDetailView.as_view(), name="shop_detail"),
]
