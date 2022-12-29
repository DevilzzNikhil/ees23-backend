from .models import Team, Event 
from rest_framework.response import Response
from .serializers import EventSerializer, TeamSerializer
from customauth.models import UserAcount
from rest_framework import generics, permissions, status




def checks(request):
    try:
        event = Event.objects.get(eventname=request.data["event"])
        leader = UserAcount.objects.get(email=request.data["leader"])
        member1 = (
            UserAcount.objects.get(email=request.data["member1"])
            if request.data["member1"]
            else None
        )
        member2 = (
            UserAcount.objects.get(email=request.data["member2"])
            if request.data["member2"]
            else None
        )
        event_teams = Team.objects.filter(eventname=event)
        first_yearites = 0
        second_yearites = 0
        if leader.year == "FIRST":
            first_yearites += 1
        elif leader.year == "SECOND":
            second_yearites += 1
        if member2:
            if member2.year == "FIRST":
                first_yearites += 1
            elif member2.year == "SECOND":
                second_yearites += 1
        if member1:
            if member1.year == "FIRST":
                first_yearites += 1
            elif member1.year == "SECOND":
                second_yearites += 1
    except Event.DoesNotExist:
        return "Event does not exist"
    except UserAcount.DoesNotExist:
        return "User does not exist"

    if (
        request.data["leader"] == request.data["member1"]
        or request.data["leader"] == request.data["member2"]
        or (
            request.data["member1"] == request.data["member2"]
            and request.data["member1"] != ""
        )
    ):
        return "Single user cannot be present twice in the team"
    elif leader != request.user and member1 != request.user and member2 != request.user:
        return "Requesting user must be a member of the team. Cannot create a team which you are not a part of."
    elif Team.objects.filter(teamname=request.data["teamname"], event=event).count():
        return "Team name already taken"
    elif (
        event_teams.filter(leader=leader).count()
        or event_teams.filter(member1=leader).count()
        or event_teams.filter(member2=leader).count()
    ):
        return "Leader already has a team in this event"
    elif (
        event_teams.filter(leader=member1).count()
        or event_teams.filter(member1=member1).count()
        or event_teams.filter(member2=member1).count()
    ) and member1 is not None:
        return "Member 1 already has a team in this event"
    elif (
        event_teams.filter(leader=member2).count()
        or event_teams.filter(member1=member2).count()
        or event_teams.filter(member2=member2).count()
    ) and member2 is not None:
        return "Member 2 already has a team in this event"
    elif (
        second_yearites != 0
        and first_yearites + second_yearites > event.members_after_1st_year
    ):
        return (
            "Max size of a not-all-1st-yearites team is "
            + str(event.members_after_1st_year)
            + " for this event"
        )
    elif second_yearites == 0 and first_yearites > event.members_from_1st_year:
        return (
            "Max size of a all-1st-yearites team is "
            + str(event.members_from_1st_year)
            + " for this event"
        )


class ViewAllEvent(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class TeamCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = TeamSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = checks(request)
        if message:
            return Response({"error": message}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        team = Team.objects.get(
            teamname=request.data["teamname"],
            event=Event.objects.get(eventname=request.data["event"]),
        )
        team_info = {
            "teamname": team.teamname,
            "event": team.event.eventname,
            "leader": team.leader.email,
            "member1": team.member1.email if team.member1 else None,
            "member2": team.member2.email if team.member2 else None,
        }

        return Response(team_info, status=status.HTTP_200_OK)

class TeamCountView(generics.GenericAPIView):

    def get(self, request):
        res = {}
        for event in Event.objects.all():
            teams = Team.objects.filter(eventname=event)
            res[event.eventname] = teams.count()
        return Response(res, status=status.HTTP_200_OK)
