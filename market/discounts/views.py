from itertools import chain

from discounts.models import ProductDiscount, CategoryDiscount, BasketDiscount
from django.views.generic import ListView


class DiscountsListView(ListView):
    """Класс представления списка всех скидок на сайте."""

    template_name = "discount/discounts-list.jinja2"
    context_object_name = "discounts"

    def get_queryset(self):
        qs1 = ProductDiscount.objects.filter(active=True)
        qs2 = CategoryDiscount.objects.filter(active=True)
        qs3 = BasketDiscount.objects.filter(active=True)

        queryset = list(chain(qs1, qs2, qs3))
        return queryset
