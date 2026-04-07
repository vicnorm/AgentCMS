import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

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
    return JsonResponse(
        {
            "html_content": page.html_content,
            "css_content": page.css_content,
            "js_content": page.js_content,
            "is_builder_page": page.is_builder_page,
        }
    )


@staff_member_required
@require_POST
def builder_save(request, page_id):
    page = get_object_or_404(Page, pk=page_id)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return HttpResponseBadRequest("Invalid JSON payload.")

    content_fields = ("html_content", "css_content", "js_content")
    max_length = 500_000

    for field in content_fields:
        value = payload.get(field, "")
        if not isinstance(value, str):
            return HttpResponseBadRequest(f"{field} must be a string.")
        if len(value) > max_length:
            return HttpResponseBadRequest(f"{field} exceeds max size.")
        setattr(page, field, value)

    page.is_builder_page = True
    page.save(update_fields=[*content_fields, "is_builder_page", "updated_at"])


    return JsonResponse({"status": "ok", "page_id": page.id})
