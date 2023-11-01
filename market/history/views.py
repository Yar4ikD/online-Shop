from django.views.generic.list import ListView
from .models import BrowsingHistory
from django.contrib.auth.mixins import LoginRequiredMixin


class HistoryView(LoginRequiredMixin, ListView):
    template_name = "history/view-histroy.jinja2"
    context_object_name = "history"

    def get_queryset(self):
        return BrowsingHistory.objects.filter(user=self.request.user)
