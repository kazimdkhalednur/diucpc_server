from rest_framework.generics import RetrieveAPIView
from .models import Certificate
from .serializers import CertificateSerializer


class CertificateRetrieveAPIView(RetrieveAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    lookup_field = "certificate_id"
    lookup_url_kwarg = "certificate_id"
