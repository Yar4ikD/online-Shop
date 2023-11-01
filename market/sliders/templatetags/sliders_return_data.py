from sliders.models import Slider
from django.template import Library


register = Library()


@register.simple_tag
def query_set():
    """Тег для возвращения данных модели Slider в шаблон jinja2."""

    sliders = Slider.objects.prefetch_related("product")

    return sliders
