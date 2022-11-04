from django.test import TestCase
from udyam_API.models import Event, Team
from custom_auth.models import UserAccount


class TestModels(TestCase):
    def setUp(self):
        self.details = {
            "teamname": "wowow",
            "event": Event.objects.create(
                eventname="mosaic", members_from_1st_year=3, members_after_1st_year=0
            ),
            "leader": UserAccount.objects.create(
                email="test_user1@example.com", password="test_password1"
            ),
            "member1": UserAccount.objects.create(
                email="test_user2@example.com", password="test_password2"
            ),
            "member2": UserAccount.objects.create(
                email="test_user3@example.com", password="test_password3"
            ),
        }

    def test_create_team(self):
        test_team = Team.objects.create(**self.details)
        self.assertEqual(Team.objects.get(teamname="wowow"), test_team)
