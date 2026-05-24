from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cms.models import Page
from .serializers import PageSerializer


# Stores the latest data received from KNIME temporarily.
# This is only used for testing/demo purposes and is not saved to the database.
latest_knime_data = []


@api_view(["GET"])
def test_knime(request):
    """
    Simple test endpoint used to verify that the API is working.
    """
    return Response({
        "message": "API works",
        "status": "ok"
    })


@api_view(["GET"])
def pages_for_knime(request):
    """
    Returns all CMS pages as JSON.

    KNIME uses this endpoint to fetch page data from AgentCMS.
    """
    pages = Page.objects.all()
    serializer = PageSerializer(pages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def receive_from_knime(request):
    """
    Receives processed data from KNIME.

    The received data is stored temporarily and printed in the Django terminal
    so the integration can be tested and verified.
    """
    global latest_knime_data

    # Save the received KNIME data temporarily in memory
    latest_knime_data = request.data

    # Print the received data in the terminal for testing/debugging
    print("Data from KNIME:")
    print(latest_knime_data)

    return Response({
        "status": "received",
        "data": latest_knime_data
    })


@api_view(["GET"])
def latest_from_knime(request):
    """
    Returns the latest data received from KNIME.

    This endpoint is only intended for testing/demo purposes.
    """
    return Response({
        "latest_knime_data": latest_knime_data
    })