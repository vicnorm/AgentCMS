from .models import Page

def menu_pages(request):
    pages = Page.objects.filter(is_published=True).order_by("title")
    return {"menu_pages": pages}
