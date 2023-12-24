from django.urls import path

from .views import *

app_name = "committees"
urlpatterns = [
    path("", CommitteListAPIView.as_view(), name="committee_list"),
    path("<str:year>/", CommitteRetrieveAPIView.as_view(), name="committee_detail"),
]
