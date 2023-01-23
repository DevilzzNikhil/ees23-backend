from django.urls import path
from .views import TeamCreateView, ViewAllEvent,TeamCountView, GetAllNoticeView

urlpatterns = [
    path("events/", ViewAllEvent.as_view(), name="get-all-events"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("team/count/", TeamCountView.as_view(), name="team-count"),
    path("updates/<str:event>", GetAllNoticeView.as_view(), name="notices"),
]