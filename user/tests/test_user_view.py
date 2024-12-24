from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewsTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "is_staff": False,
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_register_user(self):
        url = "/api/user/register/"
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "is_staff": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], data["email"])

    def test_token_obtain_pair(self):
        url = "/api/user/token/"
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        url = "/api/user/token/refresh/"
        data = {"refresh": str(refresh)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_manage_user(self):
        url = "/api/user/me/"
        token = self._get_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def _get_token(self):
        url = "/api/user/token/"
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(url, data)
        return response.data["access"]
