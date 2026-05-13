import json

from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .builder_adapter import (
    MAX_BUILDER_PAYLOAD_LENGTH,
    builder_state_for_page,
    validate_builder_payload,
)
from .models import Page


def index(request):
    pages = Page.objects.filter(is_published=True).order_by("title")
    return render(request, "cms/index.html", {"pages": pages})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "cms/page_detail.html", {"page": page})


@staff_member_required
def builder_editor(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render(request, "cms/builder_editor.html", {"page": page})


@staff_member_required
@require_GET
def builder_state(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return JsonResponse(builder_state_for_page(page))


@staff_member_required
@require_POST
def builder_save(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    if len(request.body) > MAX_BUILDER_PAYLOAD_LENGTH:
        return HttpResponseBadRequest("Payload exceeds max size.")

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON payload.")

    try:
        builder_json, rendered = validate_builder_payload(payload)
    except ValidationError as error:
        return HttpResponseBadRequest("; ".join(error.messages))

    page.builder_json = builder_json
    page.draft_html = rendered["html"]
    page.draft_css = rendered["css"]
    page.draft_js = rendered["js"]
    page.is_builder_page = True
    page.builder_updated_at = timezone.now()
    page.save(
        update_fields=[
            "builder_json",
            "draft_html",
            "draft_css",
            "draft_js",
            "is_builder_page",
            "builder_updated_at",
            "updated_at",
        ]
    )

    return JsonResponse(
        {
            "status": "ok",
            "page_id": page.id,
            "builder_updated_at": page.builder_updated_at.isoformat(),
        }
    )


@staff_member_required
@require_POST
def builder_publish(request, page_id):
    with transaction.atomic():
        page = get_object_or_404(Page.objects.select_for_update(), pk=page_id)

        if not page.builder_json:
            return HttpResponseBadRequest("Save a builder draft before publishing.")

        page.published_html = page.draft_html
        page.published_css = page.draft_css
        page.published_js = page.draft_js
        page.is_builder_page = True
        page.is_published = True
        page.builder_published_at = timezone.now()
        page.save(
            update_fields=[
                "published_html",
                "published_css",
                "published_js",
                "is_builder_page",
                "is_published",
                "builder_published_at",
                "updated_at",
            ]
        )

    return JsonResponse(
        {
            "status": "ok",
            "page_id": page.id,
            "builder_published_at": page.builder_published_at.isoformat(),
        }
    )
