from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User


class APIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("accounts:signup")
        self.login_url = reverse("accounts:login")
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            is_active=False,
        )
        self.another_user_data = {
            "username": "testanotheruser",
            "email": "testanotheruser@example.com",
            "password": "testpassword",
            "password2": "testpassword",
        }

    def test_user_signup(self):
        response = self.client.post(
            self.signup_url, self.another_user_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Check if the user was created

    def test_existing_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_info(self):
        self.client.force_authenticate(user=self.user)
        user_info_url = reverse("accounts:user_info")
        response = self.client.get(user_info_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "testuser@example.com")

    def test_user_login(self):
        # Assuming you have the URL for the token obtain endpoint
        login_url = reverse("accounts:login")
        login_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }
        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_invalid_user_verification(self):
        # Assuming you have the URL for the user verification endpoint
        invalid_verify_url = "/verify/?token=invalid_token"
        response = self.client.get(invalid_verify_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_refresh_token(self):
        # Assuming you have the URL for the token refresh endpoint
        refresh_url = reverse("accounts:token_refresh")
        refresh_data = {
            "refresh": "your_refresh_token_here",
        }
        response = self.client.post(refresh_url, refresh_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_without_authentication(self):
        user_info_url = reverse("accounts:user_info")
        response = self.client.get(user_info_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        User.objects.filter(email="testuser@example.com").delete()
