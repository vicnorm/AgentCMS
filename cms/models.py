from django.db import models
from django.utils.text import slugify
import bleach


ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "b",
    "em",
    "i",
    "u",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "ul",
    "ol",
    "li",
    "a",
    "blockquote",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel", "target"],
}


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField(blank=True)
    builder_json = models.JSONField(blank=True, default=dict)
    draft_html = models.TextField(blank=True, default="")
    draft_css = models.TextField(blank=True, default="")
    draft_js = models.TextField(blank=True, default="")
    published_html = models.TextField(blank=True, default="")
    published_css = models.TextField(blank=True, default="")
    published_js = models.TextField(blank=True, default="")
    is_builder_page = models.BooleanField(default=False)
    builder_updated_at = models.DateTimeField(blank=True, null=True)
    builder_published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def sanitized_body(self):
        return bleach.clean(
            self.body,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )

    def __str__(self):
        return self.title

    @property
    def has_builder_content(self):
        return self.has_published_builder_content

    @property
    def has_published_builder_content(self):
        return bool(
            self.is_builder_page
            and (
                self.builder_published_at
                or self.published_html.strip()
                or self.published_css.strip()
                or self.published_js.strip()
            )
        )
