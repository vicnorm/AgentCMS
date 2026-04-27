from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import json

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


class BuilderMvpTests(TestCase):
    def setUp(self):
        self.staff_user = get_user_model().objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password123",
            is_staff=True,
        )
        self.page = Page.objects.create(
            title="Builder Page",
            slug="builder-page",
            body="<p>Legacy body</p>",
            is_published=True,
        )

    def test_builder_endpoints_require_staff(self):
        editor_url = reverse("builder_editor", kwargs={"page_id": self.page.id})
        state_url = reverse("builder_state", kwargs={"page_id": self.page.id})
        save_url = reverse("builder_save", kwargs={"page_id": self.page.id})
        publish_url = reverse("builder_publish", kwargs={"page_id": self.page.id})

        self.assertEqual(self.client.get(editor_url).status_code, 302)
        self.assertEqual(self.client.get(state_url).status_code, 302)
        self.assertEqual(self.client.post(save_url, data="{}", content_type="application/json").status_code, 302)
        self.assertEqual(self.client.post(publish_url, data="{}", content_type="application/json").status_code, 302)

    def test_builder_state_starts_from_legacy_body(self):
        self.client.force_login(self.staff_user)
        state_url = reverse("builder_state", kwargs={"page_id": self.page.id})

        response = self.client.get(state_url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["source"], "legacy")
        self.assertEqual(data["builder_json"]["components"][0]["html"], "<p>Legacy body</p>")
        self.assertIn("<p>Legacy body</p>", data["draft_html"])

    def test_builder_save_reopen_publish_and_render(self):
        self.client.force_login(self.staff_user)
        save_url = reverse("builder_save", kwargs={"page_id": self.page.id})
        state_url = reverse("builder_state", kwargs={"page_id": self.page.id})
        publish_url = reverse("builder_publish", kwargs={"page_id": self.page.id})

        payload = {
            "builder_json": {
                "version": 1,
                "source": "builder",
                "components": [
                    {
                        "id": "component-1",
                        "title": "Test section",
                        "type": "html",
                        "html": "<section><h2>From Builder</h2></section>",
                        "css": ".hero{color:red;}",
                        "js": "console.log(componentRoot.dataset.builderComponentId);",
                        "reference": "Unit test",
                    }
                ],
            },
            "rendered": {
                "html": "<section><h2>From Builder</h2></section>",
                "css": ".hero{color:red;}",
                "js": "console.log('builder');",
            },
        }
        response = self.client.post(save_url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        state_response = self.client.get(state_url)
        self.assertEqual(state_response.status_code, 200)
        self.assertEqual(state_response.json()["builder_json"], payload["builder_json"])
        self.assertIn("<section><h2>From Builder</h2></section>", state_response.json()["draft_html"])
        self.assertTrue(state_response.json()["is_builder_page"])

        detail = self.client.get(reverse("page_detail", kwargs={"slug": self.page.slug}))
        self.assertContains(detail, "<p>Legacy body</p>", html=True)
        self.assertNotContains(detail, "From Builder")

        publish_response = self.client.post(publish_url, data="{}", content_type="application/json")
        self.assertEqual(publish_response.status_code, 200)

        detail = self.client.get(reverse("page_detail", kwargs={"slug": self.page.slug}))
        self.assertContains(detail, "<section><h2>From Builder</h2></section>", html=True)
        self.assertContains(detail, ".hero{color:red;}")
        self.assertContains(detail, "componentRoot")

    def test_non_builder_page_keeps_legacy_body(self):
        detail = self.client.get(reverse("page_detail", kwargs={"slug": self.page.slug}))
        self.assertContains(detail, "<p>Legacy body</p>", html=True)

    def test_builder_rejects_script_tags_in_html(self):
        self.client.force_login(self.staff_user)
        save_url = reverse("builder_save", kwargs={"page_id": self.page.id})

        payload = {
            "builder_json": {
                "version": 1,
                "components": [
                    {
                        "id": "component-1",
                        "title": "Unsafe",
                        "html": "<script>alert('x')</script>",
                        "css": "",
                        "js": "",
                        "reference": "",
                    }
                ],
            },
            "rendered": {"html": "", "css": "", "js": ""},
        }

        response = self.client.post(save_url, data=json.dumps(payload), content_type="application/json")

        self.assertEqual(response.status_code, 400)
