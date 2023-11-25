from rest_framework.serializers import ModelSerializer

from .models import *


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
