from django.db import models
from customauth.models import  UserAcount

class Event(models.Model):
    eventname = models.CharField(max_length=100, unique=True)
    members_from_1st_year = models.IntegerField()
    members_after_1st_year = models.IntegerField()

    def __str__(self):
        return self.eventname


class Team(models.Model):
    teamname = models.CharField(max_length=50, unique=True)
    eventname = models.ForeignKey(Event, on_delete=models.CASCADE)
    leader = models.ForeignKey(UserAcount, on_delete=models.CASCADE)
    member1 = models.ForeignKey(UserAcount, on_delete=models.CASCADE, null=True, blank=True, related_name='member1')
    member2 = models.ForeignKey(UserAcount, on_delete=models.CASCADE, null=True, blank=True, related_name='member2')

    def __str(self):
        return f"{self.eventname} - {self.teamname}"
