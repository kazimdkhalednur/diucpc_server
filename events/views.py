from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import EventSerializer


class EventListAPIView(ListAPIView):
    """Event list"""

    serializer_class = EventSerializer


class EventRetrieveAPIView(RetrieveAPIView):
    "Event detail with slug"
    serializer_class = EventSerializer
    lookup_field = "slug"
