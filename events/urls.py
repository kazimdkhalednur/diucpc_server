from django.urls import path

from .views import *

app_name = "events"

urlpatterns = [
    path("", EventListAPIView.as_view(), name="list"),
    path("<str:slug>/", EventRetrieveAPIView.as_view(), name="detail"),
]
