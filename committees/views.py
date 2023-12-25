from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import CommitteeSerializer


class CommitteListAPIView(ListAPIView):
    """Committe list"""

    serializer_class = CommitteeSerializer


class CommitteRetrieveAPIView(RetrieveAPIView):
    "Committe detail with slug"
    serializer_class = CommitteeSerializer
    lookup_field = "year"
