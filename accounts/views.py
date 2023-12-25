from django.conf import settings
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from .models import User
from .serializers import UserCreateSerializer, UserInfoSerializer
from .utils import activation_token, send_email


class SignUpAPIView(APIView):
    """User Sign Up API"""

    serializer_class = UserCreateSerializer

    @extend_schema(
        responses={
            201: OpenApiResponse(
                response={201},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "message": "User created successfully and verification mail is sent"  # noqa: E501
                        },
                        response_only=True,
                        status_codes=["201"],
                    ),
                ],
            ),
        }
    )
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email(request, user)
            return Response(
                {"message": "User created successfully and verification mail is sent"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyAPIView(APIView):
    """User Verify API that is triggered by clicking the link in the verification mail"""  # noqa: E501

    @extend_schema(
        responses={
            406: OpenApiResponse(
                response={406},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"error": "token is not provided"},
                        response_only=True,
                        status_codes=["406"],
                    ),
                ],
            ),
            400: OpenApiResponse(
                response={400},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"error": "Invalid token"},
                        response_only=True,
                        status_codes=["400"],
                    ),
                ],
            ),
            302: OpenApiResponse(
                response={302},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"message": "redirect to verification-success page"},
                        response_only=True,
                        status_codes=["302"],
                    ),
                ],
            ),
            202: OpenApiResponse(
                response={202},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={
                            "message": "Verify timeout. Please check your inbox. A new verification mail is sent"  # noqa: E501
                        },
                        response_only=True,
                        status_codes=["202"],
                    ),
                ],
            ),
            401: OpenApiResponse(
                response={401},
                examples=[
                    OpenApiExample(
                        "Success Response",
                        value={"error": "Invalid User"},
                        response_only=True,
                        status_codes=["401"],
                    ),
                ],
            ),
        }
    )
    def get(self, request):
        if request.GET.get("token") is None:
            return Response(
                {"error": "Token is not provided"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        try:
            received_token = request.GET["token"]
            splited_token = received_token.split(".")
            uidb64 = splited_token[0]
            token = splited_token[1]
        except IndexError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
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


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """User Retrieve Update Destroy API"""

    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return self.request.user
