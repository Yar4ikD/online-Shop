from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CatalogFiltersForm(forms.Form):
    """Форма передачи данных для фильтра. Страница каталог товаров."""

    price = forms.CharField()
    title = forms.CharField(required=False)
    available = forms.BooleanField(required=False)
    delivery = forms.BooleanField(required=False)

    def clean_price(self):
        price = self.cleaned_data.get("price")
        try:
            price_from, price_to = price.split(";")
            price_from = int(price_from)
            price_to = int(price_to)

            return price_from, price_to

        except ValueError:
            raise ValidationError(_("Ошибка формы фильтр, поле - цена"))
