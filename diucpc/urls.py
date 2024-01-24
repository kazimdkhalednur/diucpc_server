from django.urls import include, path

urlpatterns = [
    path("carousels/", include("diucpc.carousels.urls")),
    path("committees/", include("diucpc.committees.urls")),
    path("events/", include("diucpc.events.urls")),
]
