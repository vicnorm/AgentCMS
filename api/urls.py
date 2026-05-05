from django.urls import path

from .views import (
    test_knime,
    pages_for_knime,
    receive_from_knime,
    latest_from_knime,
)


urlpatterns = [
    path("test/", test_knime),
    path("pages/", pages_for_knime),
    path("receive/", receive_from_knime),
    path("latest/", latest_from_knime),
]