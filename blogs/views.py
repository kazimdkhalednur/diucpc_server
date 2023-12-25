from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Blog
from .serializers import BlogSerializer


class BlogListAPIView(ListAPIView):
    """Blog list"""

    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.published_objects.all()


class BlogRetrieveAPIView(RetrieveAPIView):
    "Blog detail with slug"
    serializer_class = BlogSerializer
    lookup_field = "slug"
