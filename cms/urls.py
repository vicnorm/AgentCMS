from django.urls import path
from .views import index, page_detail

urlpatterns = [
    path("", index, name="index"),
    path("<slug:slug>/", page_detail, name="page_detail"),
]
