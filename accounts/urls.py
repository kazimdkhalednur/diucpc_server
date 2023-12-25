from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import *

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("verify/", UserVerifyAPIView.as_view(), name="verify"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/access/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("user_info/", UserRetrieveUpdateDestroyAPIView.as_view(), name="user_info"),
]
