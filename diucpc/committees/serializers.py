from rest_framework.serializers import ModelSerializer

from .models import Committee


class CommitteeSerializer(ModelSerializer):
    class Meta:
        model = Committee
        exclude = ("id", "created_at", "updated_at", "type")
