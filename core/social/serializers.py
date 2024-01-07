from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login

from . import google
from .register import register_social_user

from core.user.serializers import UsersSerializer
from decouple import config

class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']  # type: ignore
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != config('GOOGLE_CLIENT_ID'):   # type: ignore

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']   # type: ignore
        email = user_data['email']   # type: ignore
        name = user_data['name']   # type: ignore
        provider = 'google'

        user_obj = register_social_user(provider=provider, user_id=user_id, email=email, name=name)
        refresh = TokenObtainPairSerializer.get_token(user_obj)

        data = {}
        data['user'] = UsersSerializer(user_obj).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        update_last_login(None, user_obj)  # type: ignore

        return data
