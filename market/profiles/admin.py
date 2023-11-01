from django.contrib import admin
from profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "pk", "user", "address", "phone", "balance"
    list_display_links = "pk", "user", "address", "phone", "balance"
