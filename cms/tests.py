from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Page


class PageRichTextRenderingTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123",
        )

    def test_rich_text_markup_from_admin_renders_on_page_detail(self):
        self.client.force_login(self.admin_user)

        body = """
            <h2>Section heading</h2>
            <p>This has <strong>bold text</strong>.</p>
            <ul><li>First</li><li>Second</li></ul>
        """

        response = self.client.post(
            reverse("admin:cms_page_add"),
            {
                "title": "Rich Text Page",
                "slug": "rich-text-page",
                "body": body,
                "is_published": "on",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        detail = self.client.get(reverse("page_detail", kwargs={"slug": "rich-text-page"}))

        self.assertContains(detail, "<h2>Section heading</h2>", html=True)
        self.assertContains(detail, "<strong>bold text</strong>", html=True)
        self.assertContains(detail, "<ul><li>First</li><li>Second</li></ul>", html=True)

    def test_disallowed_markup_is_sanitized_on_render(self):
        page = Page.objects.create(
            title="Unsafe",
            slug="unsafe",
            body='<p>ok</p><script>alert("xss")</script>',
            is_published=True,
        )

        detail = self.client.get(reverse("page_detail", kwargs={"slug": page.slug}))

        self.assertContains(detail, "<p>ok</p>", html=True)
        self.assertNotContains(detail, "<script>")
