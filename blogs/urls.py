from django.urls import path

from .views import *

app_name = "blogs"

urlpatterns = [
    path("", BlogListAPIView.as_view(), name="list"),
    path("<str:slug>/", BlogRetrieveAPIView.as_view(), name="detail"),
]
