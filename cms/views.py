from django.shortcuts import get_object_or_404, render
from .models import Page

def index(request):
    pages = Page.objects.filter(is_published=True).order_by("title")
    return render(request, "cms/index.html", {"pages": pages})

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, "cms/page_detail.html", {"page": page})
