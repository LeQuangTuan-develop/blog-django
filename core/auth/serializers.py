from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from core.user.serializers import UsersSerializer
from core.user.models import User,UserProfile


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UsersSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        update_last_login(None, self.user)  # type: ignore

        return data


class RegisterSerializer(UsersSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(
        required=True, write_only=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active']

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
            UserProfile.objects.create(base_user=user)
            
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user
