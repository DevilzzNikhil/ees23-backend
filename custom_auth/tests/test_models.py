from django.test import TestCase
from custom_auth.models import UserAccount


class TestModels(TestCase):
    def setUp(self):
        self.credentials = {
            "email": "test_user1@example.com",
            "password": "test_password1",
        }

    def test_create_user(self):
        test_user = UserAccount.objects.create_user(**self.credentials)
        self.assertEqual(
            UserAccount.objects.get(email="test_user1@example.com"), test_user)

    def test_create_superuser(self):
        test_superuser = UserAccount.objects.create_superuser(
            **self.credentials)
        self.assertEqual(
            UserAccount.objects.get(email="test_user1@example.com"),
            test_superuser)
        self.assertEqual(test_superuser.is_superuser, True)
