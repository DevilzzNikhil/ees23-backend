from django.test import SimpleTestCase
from django.urls import reverse, resolve
from udyam_API.views import (
    GetAllEventsView,
    WorkshopView,
    GetAllNoticeView,
    GetNoticeByIdView,
    TeamCreateView,
    TeamGetUserView,
    TeamView,
    TeamSubmissionView,
)


class TestUrls(SimpleTestCase):
    def test_get_all_evnets_url(self):
        get_all_events_url = reverse("get-all-events")
        self.assertEqual(resolve(get_all_events_url).func.view_class, GetAllEventsView)

    def test_workshop_url(self):
        workshop_url = reverse("workshop")
        self.assertEqual(resolve(workshop_url).func.view_class, WorkshopView)

    def test_get_all_notice_url(self):
        get_all_notice_url = reverse("get-all-notice")
        self.assertEqual(resolve(get_all_notice_url).func.view_class, GetAllNoticeView)

    def test_get_notice_by_id_url(self):
        get_notice_by_id_url = reverse("get-notice-by-id", args=["123"])
        self.assertEqual(
            resolve(get_notice_by_id_url).func.view_class, GetNoticeByIdView
        )

    def test_team_create(self):
        team_create_url = reverse("team-create")
        self.assertEqual(resolve(team_create_url).func.view_class, TeamCreateView)

    def test_get_teams_by_user(self):
        teams_by_user_url = reverse("teams-user")
        self.assertEqual(resolve(teams_by_user_url).func.view_class, TeamGetUserView)

    def test_team_url(self):
        team_url = reverse("team", args=["34"])
        self.assertEqual(resolve(team_url).func.view_class, TeamView)

    def test_team_submission_url(self):
        team_submission_url = reverse("team-submission")
        self.assertEqual(
            resolve(team_submission_url).func.view_class, TeamSubmissionView
        )
