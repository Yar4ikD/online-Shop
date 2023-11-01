from comments.models import Comment
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CommentAddForm(forms.ModelForm):
    """Форма добавления отзыва о товаре."""

    class Meta:
        model = Comment
        fields = ("text",)

    def clean_text(self):
        """Проверяем количество слов в тесте отзыва."""

        text: str = self.cleaned_data.get("text")
        if len(text.split()) < 2:
            raise ValidationError(_("Отзыв должен иметь минимум 2 слова."))

        return text
