# core/user/serializers.py
from core.user.models import User, UserProfile
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'last_login',
            'username',
            'user_permissions',
        ]
        extra_kwargs = {
            'email': {'validators': []},
            'username': {'validators': []}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    base_user = UserDataSerializer(many=False)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'base_user',
            'avatar',
            'gender',
        ]


class CUUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='base_user.username')

    class Meta:
        model = UserProfile
        fields = [
            'username',
            'avatar',
            'gender',
        ]

    def update(self, instance: UserProfile, validated_data):
        target_user = instance.base_user
        request_user = self.context['request'].user
        if target_user != request_user:
            raise serializers.ValidationError(
                {"auth": "you do not have permission"})

        if 'base_user' in validated_data:
            target_user_info = validated_data.pop('base_user')
            target_user.username = target_user_info.get(
                'username'
            )
            target_user.save()

        return super().update(instance, validated_data)
