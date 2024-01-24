from rest_framework.serializers import ModelSerializer
from .models import Carousels


class CarouselsSerializer(ModelSerializer):
    class Meta:
        model = Carousels
        exclude = ["id", "is_active"]