from django.db import models
from custom_auth.models import UserAccount
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Event(models.Model):
    eventname = models.CharField(max_length=20, unique=True)
    members_from_1st_year = models.IntegerField()
    members_after_1st_year = models.IntegerField()

    def __str__(self):
        return self.eventname


class Workshop(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    url = models.URLField(max_length=200)

    def __str__(self):
        string = str(self.event) + ", " + str(self.date)
        return string


class NoticeBoard(models.Model):
    title = models.TextField(blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Team(models.Model):
    teamname = models.CharField(max_length=30)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    leader = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    member1 = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="member1",
    )
    member2 = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="member2",
    )
    submission = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.event} - {self.teamname}"


class BroadCast_Email(models.Model):
    subject = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    message = RichTextUploadingField()

    def __unicode__(self):
        return self.subject

    class Meta:
        verbose_name = "BroadCast Email to all Member"
        verbose_name_plural = "BroadCast Email"
