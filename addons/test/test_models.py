from django.test import TestCase
from addons.models import Query


class TestModels(TestCase):
    def setUp(self):
        self.credentials = {
            "name": "User1",
            "email": "test_user1@example.com",
            "contact": "9876543210",
            "query": "New user query",
        }

    def test_create_query(self):
        test_user = Query.objects.create(**self.credentials)
        self.assertEqual(Query.objects.get(email="test_user1@example.com"), test_user)
