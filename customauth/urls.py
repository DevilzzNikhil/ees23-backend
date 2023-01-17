from django.urls import path
from .views import UserInitApi, LogoutView

urlpatterns = [
    path('google-login/', UserInitApi.as_view(), name='google-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]
