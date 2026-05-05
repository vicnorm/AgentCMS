from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response

from cms.models import Page
from .serializers import PageSerializer


latest_knime_data = []


@api_view(["GET"])
def test_knime(request):
    return Response({
        "message": "API funker",
        "status": "ok"
    })


@api_view(["GET"])
def pages_for_knime(request):
    pages = Page.objects.all()
    serializer = PageSerializer(pages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def receive_from_knime(request):
    global latest_knime_data

    latest_knime_data = request.data

    print("Data from KNIME:")
    print(latest_knime_data)

    return Response({
        "status": "received",
        "data": latest_knime_data
    })


@api_view(["GET"])
def latest_from_knime(request):
    return Response({
        "latest_knime_data": latest_knime_data
    })