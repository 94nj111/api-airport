from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_user_str(self):
        user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            first_name="User",
            last_name="Test",
        )
        self.assertEqual(str(user), f"{user.email}: {user.first_name} {user.last_name}")
