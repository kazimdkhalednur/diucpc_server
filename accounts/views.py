from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .models import User
from .serializers import UserCreateSerializer, UserInfoSerializer
from .utils import activation_token, send_email


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email(request, user)
            return Response(
                {"message": "User created successfully and verification is sent"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyAPIView(APIView):
    def get(self, request):
        if request.GET["token"] is None:
            return Response(
                {"error": "token is not provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        received_token = request.GET["token"]
        splited_token = received_token.split(".")
        uidb64 = splited_token[0]
        token = splited_token[1]
        account_activation_token = activation_token
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(
                settings.CLIENT_URL + "/verification-success",
                status=status.HTTP_302_FOUND,
            )
        elif user is not None and not account_activation_token.check_token(user, token):
            send_email(request, user)
            return Response(
                {
                    "message": "Verify timeout. Please check your inbox. A new verification mail is sent"  # noqa: E501
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response({"error": "Invalid User"}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
