from rest_framework import serializers
from .models import Workshop, Team, NoticeBoard, Event
from custom_auth.models import UserAccount


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class WorkshopSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()

    class Meta:
        model = Workshop
        fields = "__all__"


class NoticeBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeBoard
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    event = serializers.CharField()
    leader = serializers.EmailField()
    member1 = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    member2 = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    def save(self, **kwargs):
        data = self.validated_data
        teamname = data["teamname"]
        event = Event.objects.get(eventname=data["event"])
        leader = UserAccount.objects.get(email=data["leader"])
        member1 = (
            UserAccount.objects.get(email=data["member1"]) if data["member1"] else None
        )
        member2 = (
            UserAccount.objects.get(email=data["member2"]) if data["member2"] else None
        )
        team = Team.objects.create(
            teamname=teamname,
            event=event,
            leader=leader,
            member1=member1,
            member2=member2,
        )
        return team

    class Meta:
        model = Team
        fields = [
            "teamname",
            "event",
            "leader",
            "member1",
            "member2",
        ]


class TeamSubmissionSerializer(serializers.ModelSerializer):
    event = serializers.CharField()

    class Meta:
        model = Team
        fields = ["teamname", "event", "submission"]
