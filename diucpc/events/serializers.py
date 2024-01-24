from rest_framework.serializers import ModelSerializer

from .models import *


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ("id", "created_at", "updated_at", "status")
