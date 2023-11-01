from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = "pk", "author", "product", "text", "date_publish"
    list_display_links = "pk", "author", "product", "text", "date_publish"
