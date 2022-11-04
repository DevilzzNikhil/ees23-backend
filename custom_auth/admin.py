from django.contrib import admin

# Register your models here.
from custom_auth.models import UserAccount

admin.site.register(UserAccount)
