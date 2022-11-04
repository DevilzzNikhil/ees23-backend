from django.urls import path
from .api import UserInitApi


urlpatterns = [
    path('google-login/', UserInitApi.as_view(), name='google-login' )
]
