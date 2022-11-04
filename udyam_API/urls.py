from django.urls import path
from .views import (
    GetAllEventsView,
    WorkshopView,
    TeamView,
    TeamCreateView,
    TeamGetUserView,
    TeamSubmissionView,
    GetAllNoticeView,
    GetNoticeByIdView,
    TeamCountView,
    CertificateGetUserView,
)


urlpatterns = [
    path("events/", GetAllEventsView.as_view(), name="get-all-events"),
    path("workshop/", WorkshopView.as_view(), name="workshop"),
    path("get_all_notice/", GetAllNoticeView.as_view(), name="get-all-notice"),
    path(
        "get_notice_by_id/<int:id>",
        GetNoticeByIdView.as_view(),
        name="get-notice-by-id",
    ),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/user/", TeamGetUserView.as_view(), name="teams-user"),
    path("team/<int:id>/", TeamView.as_view(), name="team"),
    path("team/submission/", TeamSubmissionView.as_view(), name="team-submission"),
    path("team/count/", TeamCountView.as_view(), name="team-count"),
    path(
        "certificates/user", CertificateGetUserView.as_view(), name="certificates-user"
    ),
]
