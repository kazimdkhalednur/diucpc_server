from rest_framework.serializers import ModelSerializer

from .models import *


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        exclude = ("id", "created_at", "updated_at")
