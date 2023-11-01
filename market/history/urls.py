from django.urls import path
from .views import HistoryView


app_name = "history"

urlpatterns = [path("", HistoryView.as_view(), name="view_history")]
