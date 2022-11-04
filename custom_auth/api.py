from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import UserAccount

from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from typing import Tuple
from udyam_backend.settings import CLIENT_ID

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'



print(CLIENT_ID)


def google_validate_id_token(*, id_token: str) -> bool:
    # Reference: https://developers.google.com/identity/sign-in/web/backend-auth#verify-the-integrity-of-the-id-token
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )
    print(CLIENT_ID)

    if not response.ok:
        raise ValidationError('id_token is invalid.')

    audience = response.json()['aud']

    if audience != CLIENT_ID:
        raise ValidationError('Invalid audience.')

    return True


def user_create(emailCLIENT_ID, **extra_fields) -> UserAccount:
    extra_fields = {
        'is_staff': False,
        'is_active':False,
        **extra_fields
    }

    print(extra_fields)

    user = UserAccount(email=email, **extra_fields)

    user.full_clean()
    user.save()

    return user



def user_get_or_create(*, email: str, **extra_data) -> Tuple[UserAccount, bool]:
    user = UserAccount.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True


def user_get_me(*, user: UserAccount):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }


class UserInitApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        name = serializers.CharField(required=True)
        college_name = serializers.CharField(required=True)
        year = serializers.CharField(required=True)
        phone_number = serializers.CharField(required=True)

    def post(self, request, *args, **kwargs):

        id_token = request.headers.get('Authorization')
    
        google_validate_id_token(id_token=id_token)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, bool = user_get_or_create(**serializer.validated_data)
        print(request.data)

        response = Response(data=user_get_me(user=user))
        register_response = Response("You have registered Suceesfully")
        login_response = Response("You have logged in successfully")
        if bool :
            return register_response
        else :
            return login_response

