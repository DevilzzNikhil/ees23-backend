from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from custom_auth.models import UserAccount


class TestView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.credentials_user1 = {
            "email": "test_user1@example.com",
            "password": "test_password1",
        }
        self.test_user1 = UserAccount.objects.create_user(**self.credentials_user1)
        self.test_user1.name = "test_user1_name"
        self.test_user1.year = "2nd year"
        self.test_user1.college_name = "IIT BHU"
        self.test_user1.referral_count = 2
        self.test_user1.save()

        self.credentials_user2 = {
            "email": "test_user2@example.com",
            "password": "test_password2",
        }
        self.test_user2 = UserAccount.objects.create_user(**self.credentials_user2)
        self.test_user2.name = "test_user2_name"
        self.test_user2.year = "2nd year"
        self.test_user2.college_name = "IIT BHU"
        self.test_user2.referral_code = self.test_user1.user_referral_code
        self.test_user2.referral_count = 3
        self.test_user2.save()

        self.credentials = {
            "name": "User1",
            "email": "test_user1@example.com",
            "contact": "9876543210",
            "query": "New user query",
        }

        self.query_url = reverse("query")
        self.referral_url = reverse("referral")

    # Test Query View
    def test_query_view_200(self):
        response = self.client.post(
            self.query_url,
            self.credentials,
        )
        self.assertEqual(response.status_code, 200)

    # Test Referral View
    def test_referral_view_200(self):
        response = self.client.get(self.referral_url)
        self.assertEqual(response.status_code, 200)
