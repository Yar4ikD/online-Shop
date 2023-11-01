from django.contrib import admin
from sliders.models import Slider, Banner


class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "product",
        "image",
    )
    list_filter = (
        "id",
        "title",
    )


class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "image",
    )
    list_filter = (
        "id",
        "title",
    )


admin.site.register(Slider, SliderAdmin)
admin.site.register(Banner, BannerAdmin)
