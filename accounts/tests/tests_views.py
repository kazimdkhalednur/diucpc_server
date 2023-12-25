from time import sleep

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import User
from ..utils import activation_token, profile_photo_path

fake = Faker()


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
        new_user_data = self.user_data.copy()
        new_user_data["password2"] = fake.password()
        response = self.client.post(self.signup_url, new_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], "Password doesn't match")


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

    def test_user_info_without_authentication(self):
        response = self.client.get(self.user_info_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_get_user_info(self):
        login_url = reverse("accounts:login")
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

        response = self.client.get(self.user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile_photo_url = profile_photo_path(
            self.user, self.user_data["profile_photo"].name
        )
        self.assertTrue(response.data["profile_photo"].endswith(profile_photo_url))

        temp_user_data = self.user_data.copy()
        temp_user_data.pop("profile_photo")

        self.assertTrue(self.user.check_password(temp_user_data.pop("password")))
        for key, value in temp_user_data.items():
            self.assertEqual(response.data[key], value)
        self.assertEqual(response.data["role"], "general")

    def test_get_user_info_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = self.client.get(self.user_info_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_update(self):
        login_url = reverse("accounts:login")
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

        update_data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "username": fake.user_name(),
            "role": fake.random_element(
                elements=(choices[0] for choices in User.USER_ROLE_CHOICES)
            ),
            "profile_photo": SimpleUploadedFile(
                name="update_images.png",
                content=open(self.image_path, "rb").read(),
                content_type="image/png",
            ),
        }
        response = self.client.patch(
            self.user_info_url, update_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_user = User.objects.get(email=self.user_data["email"])
        profile_photo_url = profile_photo_path(
            update_user, update_data["profile_photo"].name
        )
        self.assertTrue(response.data["profile_photo"].endswith(profile_photo_url))
        update_data.pop("profile_photo")

        for key, value in update_data.items():
            self.assertEqual(response.data[key], value)

    def test_user_update_email(self):
        login_url = reverse("accounts:login")
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

        update_data = {
            "email": fake.email(),
        }
        response = self.client.patch(self.user_info_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotEqual(response.data["email"], update_data["email"])

    def tearDown(self):
        self.user.profile_photo.delete()


class TokenObtainPairViewAPIView(APITestCase):
    """Test for TokenObtainPairViewAPIView"""

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
    login_url = reverse("accounts:login")

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self):
        login_data = {
            "email": self.user_data["email"],
            "password": fake.password(),
        }
        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )

    def tearDown(self):
        self.user.profile_photo.delete()


class TokenRefreshViewAPIView(APITestCase):
    """Test for TokenRefreshViewAPIView"""

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
    login_url = reverse("accounts:login")
    refresh_url = reverse("accounts:token_refresh")

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_refresh_token(self):
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        refresh_token = response.data["refresh"]
        response = self.client.post(
            self.refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_with_invalid_token(self):
        response = self.client.post(
            self.refresh_url, {"refresh": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Token is invalid or expired")

    def tearDown(self):
        self.user.profile_photo.delete()


class TokenVerifyViewAPIView(APITestCase):
    """Test for TokenVerifyViewAPIView"""

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
    login_url = reverse("accounts:login")
    verify_url = reverse("accounts:token_verify")

    def setUp(self):
        self.user = User.objects.create_user(**self.user_data)

    def test_verify_token(self):
        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        access_token = response.data["access"]
        response = self.client.post(
            self.verify_url, {"token": access_token}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token_with_invalid_token(self):
        response = self.client.post(
            self.verify_url, {"token": "invalid_token"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Token is invalid or expired")

    def tearDown(self):
        self.user.profile_photo.delete()
