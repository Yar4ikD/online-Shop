import random

from django.core.cache import cache
from django.template import Library
from sliders.models import Banner

register = Library()


@register.simple_tag
def query_set():
    """Тег для возвращения данных модели Banner в шаблон jinja2."""

    banners = cache.get("banners")

    if not banners:
        banners = Banner.objects.values_list("pk", flat=True)
        banners = Banner.objects.filter(pk__in=random.choices(banners, k=3))
        cache.set("banners", banners, 600)

    return banners
