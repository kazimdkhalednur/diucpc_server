from django.urls import path
from . import views

app_name = "certificates"
urlpatterns = [
    path("<str:certificate_id>/", views.CertificateRetrieveAPIView.as_view(), name="get"),
]