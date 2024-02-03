from .models import Certificate
from rest_framework.serializers import ModelSerializer


class CertificateSerializer(ModelSerializer):
    class Meta:
        model = Certificate
        fields = "__all__"