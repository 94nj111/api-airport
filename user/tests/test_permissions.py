from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User
from airport.permissions import IsAdminOrIfAuthenticatedReadOnly


class PermissionTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com", password="userpassword"
        )
        self.url = "/api/airport/airplanes/"

    def test_permission_for_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_for_authenticated_user_post(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_for_authenticated_user_get(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
