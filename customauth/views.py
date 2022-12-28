from rest_framework import serializers, generics, status, permissions
# from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAcount
# from django.conf import settings
# from django.http import HttpResponse
from django.core.exceptions import ValidationError
from typing import Tuple
from udyamBackend.settings import CLIENT_ID
import requests
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token


GOOGLE_ID_TOKEN_INFO_URL = 'https://oauth2.googleapis.com/tokeninfo'

def google_validate(*, id_token: str, email:str) -> bool:

    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': id_token}
    )

    if not response.ok:
        raise ValidationError('Id token is invalid')

    audience = response.json()['aud']
    if audience != CLIENT_ID:
        raise ValidationError("Invalid Audience")

    if (response.json())["email"]!=email:
        raise ValidationError('Email mismatch')

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

def user_get_me(*, user: UserAcount):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'message': "Your registration was successful!",
    }


class UserInitApi(generics.GenericAPIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        name = serializers.CharField(required=True)
        college_name = serializers.CharField(required=True)
        year = serializers.CharField(required=True)
        phone_number = serializers.CharField(required=True)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        id_token = request.headers.get('Authorization')
        email = request.data.get("email")
        google_validate(id_token=id_token,email=email)

        if UserAcount.objects.filter(email=email).count()==0:
            serializer = self.InputSerializer(data=request.data)
            if not serializer.is_valid():
                error = {}
                for err in serializer.errors:
                    error[err] = serializer.errors[err][0]
                return Response(error, status=status.HTTP_409_CONFLICT)
            user, bool = user_get_or_create(**serializer.validated_data)
        
        response = Response(data=user_get_me(user=UserAcount.objects.get(email=email)))
        token,_ = Token.objects.get_or_create(user = user)

        return Response({"token" : token.key})


class LogoutView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated)

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

            
