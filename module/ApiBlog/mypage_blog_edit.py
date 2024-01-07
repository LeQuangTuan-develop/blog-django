from rest_framework import serializers
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import *


class MypageBlogSerializer(serializers.ModelSerializer):
    thumbnail_image_url = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source="created_by.username")
    author_info = serializers.SerializerMethodField()

    def get_thumbnail_image_url(self, obj: Blog):
        return obj.thumbnail_image.url if obj.thumbnail_image else '' or 'no_image'

    def get_author_info(self, obj):
        return {
            "author_id": obj.created_by.id,
            "avatar": obj.created_by.profile.avatar.url,
        }

    class Meta:
        model = Blog
        fields = [
            'id',
            'author',
            'author_info',
            'name',
            'sub_title',
            'description',
            'html_string',
            'thumbnail_image_url',
            'series',
            'domain',
            'created_at',
            'updated_at',
            'created_by',
            'is_valid',
            'is_modified',
            'view_count',
            'like_count',
            'status_type'
        ]
        read_only_fields = ('created_at', 'updated_at',
                            'created_by', 'is_modified', 'is_valid', 'view_count')


class MypageBlogCUSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = [
            'id',
            'name',
            'sub_title',
            'description',
            'html_string',
            'thumbnail_image',
            'series',
            'domain',
            'created_at',
            'updated_at',
            'created_by',
            'is_valid',
            'is_modified',
            'view_count',
            'like_count',
            'status_type'
        ]
        read_only_fields = ('created_at', 'updated_at',
                            'created_by', 'is_modified', 'is_valid', 'view_count')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        if 'fxeater' in self.context['request'].stream.path:
            validated_data['domain'] = 2

        new_blog = Blog.objects.create(**validated_data)

        return new_blog

    def update(self, instance: Blog, validated_data):
        if instance.created_by != self.context['request'].user and not self.context['request'].user.is_superuser:
            error = {
                'message': 'you do not have the right'
            }
            raise serializers.ValidationError(error)

        if not 'thumbnail_image' in validated_data:
            validated_data['thumbnail_image'] = instance.thumbnail_image
        else:
            validated_data['thumbnail_image'] = validated_data['thumbnail_image'] or instance.thumbnail_image
        instance.updated_at = timezone.now()
        instance.save()

        return super().update(instance, validated_data)


class MypageBlogViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Blog.objects.filter(is_valid=1, domain=DOMAIN_FXEATER).order_by('-created_at')
        return Blog.objects.filter(
            is_valid=1, domain=DOMAIN_FXEATER, created_by=user).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MypageBlogSerializer

        return MypageBlogCUSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # check if request user is admin or author
        request_user = request.user
        target_blog = Blog.objects.get(id=kwargs['pk'])
        if target_blog.created_by == request_user or request_user.is_superuser:
            target_blog.is_valid = 0
            target_blog.save()

            return Response(data='delete success')
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)
