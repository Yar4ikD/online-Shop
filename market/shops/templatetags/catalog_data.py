from django.core.cache import cache
from products.models import Category
from django.template import Library

register = Library()


@register.simple_tag
def query_set():
    """Тег для возвращения данных модели Category в шаблон jinja2."""

    category = cache.get("cat")

    if not category:
        category = Category.objects.prefetch_related("parent").order_by("pk")
        cache.set("cat", category, 86400)

    return category
