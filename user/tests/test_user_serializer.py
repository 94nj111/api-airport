from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.user_data["email"])
        self.assertTrue(user.check_password(self.user_data["password"]))

    def test_create_user_invalid_password(self):
        invalid_data = {
            "email": "testuser@example.com",
            "password": "123",
        }
        serializer = UserSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_update_user(self):
        user = get_user_model().objects.create_user(**self.user_data)
        updated_data = {"password": "newpassword"}
        serializer = UserSerializer(user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password(updated_data["password"]))
