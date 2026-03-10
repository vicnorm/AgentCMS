from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE

from .models import Page


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = "__all__"
        widgets = {
            "body": TinyMCE(
                attrs={"cols": 80, "rows": 24},
                mce_attrs={
                    "menubar": False,
                    "plugins": "lists link",
                    "toolbar": "undo redo | formatselect | bold italic | bullist numlist | link",
                },
            )
        }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    form = PageAdminForm
    list_display = ("title", "slug", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
