from django.urls import path
from .views import UserInitApi

urlpatterns = [
    path('google-login/', UserInitApi.as_view(), name='google-login'),
]
