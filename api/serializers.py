from rest_framework import serializers
from cms.models import Page


class PageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Page model.

    This class converts Page model instances into JSON format so they can be
    sent through the AgentCMS API and used by external tools such as KNIME.
    """

    class Meta:
        # The Django model that this serializer is based on
        model = Page

        # Include all fields from the Page model in the API response
        fields = "__all__"