from django import test
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from custom_auth.models import UserAccount
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.authtoken.models import Token
from udyam_API.models import NoticeBoard, Team, Event


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
        self.test_user1.save()
        self.test_user2 = UserAccount.objects.create_user(
            email="test_user2@example.com", password="test_password2"
        )
        self.test_user3 = UserAccount.objects.create_user(
            email="test_user3@example.com", password="test_password3"
        )

        self.credentials_user4 = {
            "email": "test_user4@example.com",
            "password": "test_password4",
        }
        self.test_user4 = UserAccount.objects.create_user(**self.credentials_user4)
        self.test_event1 = Event.objects.create(
            eventname="spybits", members_from_1st_year=3, members_after_1st_year=2
        )

        self.auth_token = Token.objects.get_or_create(user=self.test_user1)
        self.uidb64 = urlsafe_base64_encode(smart_bytes(self.test_user1.id))
        self.token = PasswordResetTokenGenerator().make_token(self.test_user1)

        self.notice1_data = {
            "title": "notice1",
            "description": "notice1_description",
        }
        self.notice1 = NoticeBoard.objects.create(**self.notice1_data)
        self.id = self.notice1.id

        self.team1_details = {
            "teamname": "Team One",
            "event": "spybits",
            "leader": "test_user1@example.com",
            "member1": "test_user2@example.com",
            "member2": "test_user3@example.com",
        }
        self.team1_creation_details = {
            "teamname": "Team One",
            "event": self.test_event1,
            "leader": self.test_user1,
            "member1": self.test_user2,
            "member2": self.test_user3,
        }
        self.team1 = Team.objects.create(**self.team1_creation_details)

        self.team1_submission_data = {
            "teamname": "Team One",
            "event": "spybits",
            "submission": "submission.com",
        }

        self.team2_details = {
            "teamname": "Team Two",
            "event": "spybits",
            "leader": "test_user4@example.com",
            "member1": "",
            "member2": "",
        }

        self.get_all_events_url = reverse("get-all-events")
        self.workshop_url = reverse("workshop")
        self.get_all_notice_url = reverse("get-all-notice")
        self.get_notice_by_id_url1 = reverse("get-notice-by-id", args=[self.id])
        self.get_notice_by_id_url2 = reverse("get-notice-by-id", args=["123"])
        self.team_create_url = reverse("team-create")
        self.teams_by_user_url = reverse("teams-user")
        self.team_url = reverse("team", args=["1"])
        self.team_submission_url = reverse("team-submission")

    def test_get_all_events_view(self):
        response = self.client.get(self.get_all_events_url)
        self.assertEqual(response.status_code, 200)

    # get data from WorkshopView
    def test_workshop_view_get(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(self.workshop_url)
        self.assertEqual(response.status_code, 200)

    def test_get_all_notice_view(self):
        response = self.client.get(self.get_all_notice_url)
        self.assertEqual(response.status_code, 200)

    def test_get_notice_by_id_view_200(self):
        response = self.client.get(self.get_notice_by_id_url1)
        self.assertEqual(response.status_code, 200)

    def test_get_notice_by_id_view_404(self):
        response = self.client.get(self.get_notice_by_id_url2)
        self.assertEqual(response.status_code, 404)

    def test_team_create_view_200(self):
        self.client.force_authenticate(user=self.test_user4)
        response = self.client.post(self.team_create_url, self.team2_details)
        self.assertEqual(response.status_code, 200)

    def test_team_create_view_403(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.post(self.team_create_url, self.team1_details)
        self.assertEqual(response.status_code, 403)

    def test_team_get_user_view_200(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(self.teams_by_user_url)
        self.assertEqual(response.status_code, 200)

    def test_team_view_get_200(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(self.team_url)
        self.assertEqual(response.status_code, 200)

    def test_team_view_get_404(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(reverse("team", args=["123"]))
        self.assertEqual(response.status_code, 404)

    def test_team_view_patch_200(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.patch(self.team_url, self.team1_details)
        self.assertEqual(response.status_code, 200)

    def test_team_view_delete_200(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.delete(self.team_url)
        self.assertEqual(response.status_code, 200)

    def test_team_view_delete_404(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.delete(reverse("team", args=["123"]))
        self.assertEqual(response.status_code, 404)

    def test_team_view_delete_403(self):
        self.client.force_authenticate(user=self.test_user4)
        response = self.client.delete(self.team_url)
        self.assertEqual(response.status_code, 403)

    def test_team_submission_view_post_200(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.post(
            self.team_submission_url, self.team1_submission_data
        )
        self.assertEqual(response.status_code, 200)

    def test_team_submission_view_403(self):
        self.client.force_authenticate(user=self.test_user4)
        response = self.client.post(
            self.team_submission_url, self.team1_submission_data
        )
        self.assertEqual(response.status_code, 403)
