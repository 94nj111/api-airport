from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


class UserViewsTestCase(APITestCase):
    REGISTER_URL = reverse("user:register")
    TOKEN_OBTAIN_URL = reverse("user:token_obtain_pair")
    TOKEN_REFRESH_URL = reverse("user:token_refresh")
    MANAGE_USER_URL = reverse("user:me")

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "is_staff": False,
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_register_user(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "is_staff": False,
        }
        response = self.client.post(self.REGISTER_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_token_obtain_pair(self):
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.TOKEN_OBTAIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        data = {"refresh": str(refresh)}
        response = self.client.post(self.TOKEN_REFRESH_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_manage_user(self):
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(self.MANAGE_USER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def _get_token(self):
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.TOKEN_OBTAIN_URL, data)
        return response.data["access"]
