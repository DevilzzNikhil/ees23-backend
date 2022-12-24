from django.urls import path
from .views import UserInitApi,broadcast_mail

urlpatterns = [
    path('google-login/', UserInitApi.as_view(), name='google-login'),
    path("broadcast/<subject>/", broadcast_mail, name="broadcast_mail"),
    
]
