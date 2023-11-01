from django import forms
from .models import Delivery, Order
from django.utils.translation import gettext_lazy as _


class OrderStep1Form(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            "customer": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": _("Введите имя, фамилию и отчество"),
                    "required": True,
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": _("Введите телефон"),
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": _("Введите почту"),
                    "required": True,
                }
            ),
        }

        fields = "customer", "email", "phone"


class OrderStep2Form(forms.ModelForm):
    class Meta:
        model = Delivery
        widgets = {
            "delivery_type": forms.RadioSelect(attrs={"class": "toggle-box"}),
            "city": forms.TextInput(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": _("Введите город доставки"),
                    "required": True,
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-input border-custom",
                    "placeholder": _("Введите адрес доставки"),
                    "required": True,
                    "rows": 3,
                    "cols": 3,
                }
            ),
        }

        fields = "delivery_type", "city", "address"


class OrderStep3Form(forms.ModelForm):
    class Meta:
        model = Delivery
        widgets = {
            "pay": forms.RadioSelect(attrs={"class": "toggle-box"}),
        }

        fields = ("pay",)
