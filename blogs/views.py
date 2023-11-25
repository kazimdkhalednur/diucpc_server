from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import BlogSerializer


class BlogListAPIView(ListAPIView):
    """Blog list"""

    serializer_class = BlogSerializer


class BlogRetrieveAPIView(RetrieveAPIView):
    "Blog detail with slug"
    serializer_class = BlogSerializer
    lookup_field = "slug"
