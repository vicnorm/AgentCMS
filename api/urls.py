from django.urls import path

from .views import (
    test_knime,
    pages_for_knime,
    receive_from_knime,
    latest_from_knime,
)


# URL routes for the AgentCMS KNIME integration API
urlpatterns = [
    # Simple test endpoint used to check that the API is running
    path("test/", test_knime),

    # Returns CMS page data as JSON so KNIME can retrieve it
    path("pages/", pages_for_knime),

    # Receives processed data sent back from KNIME
    path("receive/", receive_from_knime),

    # Shows the latest data received from KNIME for testing/demo purposes
    path("latest/", latest_from_knime),
]