from django.urls import path
from .views import ProductDetailView, UploadFileView


app_name = "products"

urlpatterns = [
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("upload-file", UploadFileView.as_view(), name="upload_file"),
]
