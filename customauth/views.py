from rest_framework import serializers, generics
# from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAcount
# from django.conf import settings
# from django.http import HttpResponse
from django.core.exceptions import ValidationError
from typing import Tuple
from udyamBackend.settings import CLIENT_ID
import requests
# from django.contrib.auth import login, logout
# from rest_framework.authtoken.models import Token


GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

def google_validate(*, id_token: str) -> bool:

    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )

    if not response.ok:
        raise ValidationError('Id token is invalid')

    audience = response.json()['aud']
    if audience != CLIENT_ID:
        raise ValidationError("Invalid Audience")

    return True


def user_create(email, **extra_field) -> UserAcount:
    # print(extra_field)
    extra_fields = {
        'is_staff': False,
        'is_active': True,
        **extra_field
    }

    print(extra_fields)

    user = UserAcount(email=email, **extra_fields)
    user.save()
    return user


def user_get_or_create(*, email: str, **extra_data) -> Tuple[UserAcount, bool]:
    # print(email)
    user = UserAcount.objects.filter(email=email).first()

    if user:
        return user, False
    # print(extra_data)
    return user_create(email=email, **extra_data), True

def user_get_me(*, user: UserAcount, bool):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'message': "You have registered Suceesfully" if bool else "You have logged in successfully",
    }

class UserInitApi(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        name = serializers.CharField(required=True)
        college_name = serializers.CharField(required=True)
        year = serializers.CharField(required=True)
        phone_number = serializers.CharField(required=True)

    def post(self, request, *args, **kwargs):
        id_token = request.headers.get('Authorization')
        google_validate(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, bool = user_get_or_create(**serializer.validated_data)
        # login(request=request,user=user)
        print("loggin sucess")

        response = Response(data=user_get_me(user=user, bool=bool))
        if bool:
            return response
        else:
            return response
