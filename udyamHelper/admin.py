from django.contrib import admin

# Register your models here.
from .models import Team, Event
admin.site.register(Team)
admin.site.register(Event)

