from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Page


class PageDetailViewTests(TestCase):
    def test_published_page_with_image_displays_image(self):
        image_content = (
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00"
            b"\x01\x00\x01\x00\x00\x02\x02\x4c\x01\x00\x3b"
        )
        page = Page.objects.create(
            title="About",
            slug="about",
            body="Welcome to the site.",
            is_published=True,
            image=SimpleUploadedFile("about.gif", image_content, content_type="image/gif"),
            image_alt_text="About page hero",
        )

        response = self.client.get(reverse("page_detail", args=[page.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'src="{page.image.url}"')
        self.assertContains(response, 'alt="About page hero"')
