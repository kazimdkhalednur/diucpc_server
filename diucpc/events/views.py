from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Event
from .serializers import EventSerializer


class EventPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"


class EventListAPIView(ListAPIView):
    """Event list"""

    serializer_class = EventSerializer
    queryset = Event.objects.published()
    pagination_class = EventPagination


class EventRetrieveAPIView(RetrieveAPIView):
    """Event detail with slug"""

    serializer_class = EventSerializer
    queryset = Event.objects.published()
    lookup_field = "slug"
