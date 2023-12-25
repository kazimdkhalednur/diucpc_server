from time import sleep

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from .models import User
from .utils import activation_token, profile_photo_path

fake = Faker()


class UserModelTestCase(TestCase):
    """Test for User Model"""

    image_path = settings.BASE_DIR / "test/pictures/images.png"
    user_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake.password(),
        "role": fake.random_element(
            elements=("general", "associative", "executive", "core")
        ),
        "profile_photo": SimpleUploadedFile(
            name="images.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        ),
    }

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        temp_user_data = self.user_data.copy()
        temp_user_data.pop("profile_photo")

        self.assertTrue(self.user.check_password(temp_user_data.pop("password")))
        self.assertEqual(
            self.user.profile_photo.url,
            settings.MEDIA_URL
            + profile_photo_path(self.user, self.user_data["profile_photo"].name),
        )
        for key, value in temp_user_data.items():
            self.assertEqual(getattr(self.user, key), value)

    def test_user_count(self):
        self.assertEqual(User.objects.count(), 1)

    def test_user_delete(self):
        self.user.delete()
        self.assertEqual(User.objects.count(), 0)

    def test_user_default_role(self):
        user = User.objects.create_user(
            email=fake.email(),
            username=fake.name(),
            password=fake.password(),
        )
        self.assertEqual(user.role, "general")

    def tearDown(self):
        self.user.profile_photo.delete()


class SignUpAPIViewTestCase(APITestCase):
    """Test for SignUpAPIView"""

    fake_password = fake.password()
    user_data = {
        "first_name": fake.name(),
        "last_name": fake.name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake_password,
        "password2": fake_password,
    }
    signup_url = reverse("accounts:signup")

    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["message"],
            "User created successfully and verification mail is sent",
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.get(email=self.user_data["email"]).is_active)

    def test_existing_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        response = self.client.post(self.signup_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"][0], "A user with that username already exists."
        )
        self.assertEqual(
            response.data["email"][0], "user with this email already exists."
        )

    def test_user_signup_with_invalid_data(self):
        try:
            new_user_data = self.user_data.copy()
            new_user_data["password2"] = fake.password()
            response = self.client.post(self.signup_url, new_user_data, format="json")
        except ValidationError as e:
            self.assertEqual(e.args[0].detail, {"password": "Password doesn't match"})
        finally:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserVerifyAPIViewTestCase(APITestCase):
    """Test for UserVerifyAPIView"""

    fake_password = fake.password()
    user_data = {
        "first_name": fake.name(),
        "last_name": fake.name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake_password,
        "password2": fake_password,
    }
    signup_url = reverse("accounts:signup")

    def test_user_verify_without_token(self):
        verify_url = reverse("accounts:verify")
        response = self.client.get(verify_url)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data["error"], "Token is not provided")

    def test_user_verify_invalid_token(self):
        verify_url = reverse("accounts:verify")
        response = self.client.get(verify_url, {"token": "invalid_token"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid token")

    def test_user_verify(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        user = User.objects.get(email=self.user_data["email"])
        uid = urlsafe_base64_encode(force_bytes(user.id))
        verify_url = reverse("accounts:verify")
        token = uid + "." + activation_token.make_token(user)
        response = self.client.get(verify_url, {"token": token})

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, settings.CLIENT_URL + "/verification-success")
        self.assertTrue(User.objects.get(email=self.user_data["email"]).is_active)

    def test_user_verify_timeout(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        user = User.objects.get(email=self.user_data["email"])
        settings.PASSWORD_RESET_TIMEOUT = 0.5  # Set timeout to 0.5 second
        uid = urlsafe_base64_encode(force_bytes(user.id))
        verify_url = reverse("accounts:verify")
        token = uid + "." + activation_token.make_token(user)
        sleep(1)  # Wait for 1 seconds
        response = self.client.get(verify_url, {"token": token})

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(
            response.data["message"],
            "Verify timeout. Please check your inbox. A new verification mail is sent",
        )
        self.assertFalse(User.objects.get(email=self.user_data["email"]).is_active)

    def test_user_verify_invalid_user(self):
        verify_url = reverse("accounts:verify")
        response = self.client.post(self.signup_url, self.user_data, format="json")
        user = User.objects.get(email=self.user_data["email"])
        uid = urlsafe_base64_encode(force_bytes(100))  # Invalid user id
        token = uid + "." + activation_token.make_token(user)
        response = self.client.get(verify_url, {"token": token})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid User")

    def tearDown(self):
        User.objects.filter(email=self.user_data["email"]).delete()


class UserInfoAPIViewTestCase(APITestCase):
    """Test for UserInfoAPIView"""

    image_path = settings.BASE_DIR / "test/pictures/images.png"
    user_data = {
        "first_name": fake.name(),
        "last_name": fake.name(),
        "email": fake.email(),
        "username": fake.user_name(),
        "password": fake.password(),
        "profile_photo": SimpleUploadedFile(
            name="images.png",
            content=open(image_path, "rb").read(),
            content_type="image/png",
        ),
    }
    user_info_url = reverse("accounts:user_info")

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def login(self):
        login_url = reverse("accounts:login")
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_user_info_without_authentication(self):
        response = self.client.get(self.user_info_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_user_info(self):
        self.login()

        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if settings.DEBUG:
            request = response.request
            protocol = "https" if request.is_secure() else "http"
            domain = get_current_site(request).domain
            self.assertEqual(
                response.data["profile_photo"],
                protocol
                + "://"
                + domain
                + settings.MEDIA_URL
                + profile_photo_path(self.user, self.user_data["profile_photo"].name),
            )

        temp_user_data = self.user_data.copy()
        temp_user_data.pop("password")
        temp_user_data.pop("profile_photo")
        response.data.pop("profile_photo")

        for key, value in temp_user_data.items():
            self.assertEqual(response.data[key], value)
        self.assertEqual(response.data["role"], "general")

    def tearDown(self):
        User.objects.filter(email=self.user_data["email"]).delete()
