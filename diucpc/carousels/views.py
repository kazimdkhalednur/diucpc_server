from rest_framework.generics import ListAPIView

from .models import Carousels
from .serializers import CarouselsSerializer


class CarouselListAPIView(ListAPIView):
    """Carousel list"""

    serializer_class = CarouselsSerializer
    queryset = Carousels.objects.active()


