from django.contrib import admin
from .models import Page
# Register your models here.
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}