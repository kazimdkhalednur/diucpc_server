from django.urls import path

from . import views

app_name = "carousels"
urlpatterns = [
    path("", views.CarouselListAPIView.as_view(), name="list"),
]
