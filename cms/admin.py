from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
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
    list_display = ("title", "slug", "is_published", "is_builder_page", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("builder_editor_link",)
    fields = (
        "title",
        "slug",
        "body",
        "html_content",
        "css_content",
        "js_content",
        "is_builder_page",
        "is_published",
        "builder_editor_link",
    )

    def builder_editor_link(self, obj):
        if not obj or not obj.pk:
            return "Save this page first to open the builder editor."
        url = reverse("builder_editor", kwargs={"page_id": obj.pk})
        return format_html('<a class="button" href="{}">Open Builder Editor</a>', url)

    builder_editor_link.short_description = "Builder"
