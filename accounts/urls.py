from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = "accounts"

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("verify/", UserVerifyAPIView.as_view(), name="verify"),
    path("token/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user_info/", UserInfoAPIView.as_view(), name="user_info"),
]
