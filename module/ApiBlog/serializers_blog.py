from rest_framework import serializers
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

from core.user.models import UserProfile, User

from .models import *
from module.utils import get_support_lang


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class UserDataSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'last_login',
            'username',
            'profile'
        ]


class GetReplyBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyBlog
        fields = '__all__'


class PostUpdateReplyBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReplyBlog
        fields = '__all__'

    def create(self, validated_data):
        request_data = validated_data

        validated_data = {}  # reset data to leave other fields as default

        validated_data['created_by'] = self.context['request'].user
        validated_data['content'] = request_data['content']
        validated_data['target_blog'] = request_data['target_blog']

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # only allow update content

        # check permisstion
        request_user = self.context['request'].user

        if request_user == instance.created_by or request_user.is_superuser:

            instance.content = validated_data['content']
            instance.updated_at = datetime.datetime.now()
            instance.is_modified = 1
            instance.save()

            return instance
        error = {'data': 'you do not have permission'}
        raise serializers.ValidationError(error)


class BlogSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source="created_by.username")
    author_info = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    thumbnail_image_url = serializers.SerializerMethodField()
    related_blog = serializers.SerializerMethodField()

    def get_author_info(self, obj):
        return {
            "author_id": obj.created_by.id,
            "avatar": obj.created_by.profile.avatar.url,
        }

    def get_replies(self, obj):
        reply_obj = ReplyBlog.objects.filter(target_blog=obj)
        out_data = []
        if reply_obj:
            for _r in reply_obj:
                if _r.is_valid == 1:
                    out_data.append({
                        'content': _r.content,
                        'created_at': _r.created_at,
                        'author': _r.get_author_info()
                    })
        return out_data

    def get_thumbnail_image_url(self, obj: Blog):
        return obj.thumbnail_image.url if obj.thumbnail_image else '' or 'no_image'

    def get_related_blog(self, obj: Blog):
        series_id = obj.series.pk if obj.series else None
        if not series_id:
            return []
        else:
            blogs_obj = Blog.objects.filter(
                series_id=series_id).order_by('-id')
            out_data = []
            target_lang = get_support_lang(
                self.context['request'].query_params)
            if blogs_obj:
                for _b in blogs_obj:
                    out_data.append({
                        'id': _b.pk,
                        'name': _b.get_name_by_lang(target_lang),
                    })
            return out_data

    class Meta:
        model = Blog
        fields = [
            'id',
            'created_at',
            'status_type',
            'author',
            'author_info',
            'related_blog',
            'thumbnail_image_url',

            'description',
            'html_string',
            'name',
            'sub_title',

            'description_ja',
            'html_string_ja',
            'name_ja',
            'sub_title_ja',

            'description_es',
            'html_string_es',
            'name_es',
            'sub_title_es',

            'description_cn',
            'html_string_cn',
            'name_cn',
            'sub_title_cn',

            'view_count',
            'like_count',
            'replies'
        ]
        read_only_fields = ('created_at', 'created_by')

    # nothing to do here
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(BlogSerializer, self).__init__(*args, **kwargs)

    # filter + modify final output here
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        target_lang = get_support_lang(self.context['request'].query_params)

        return self.modify_output(ret, target_lang)

    def modify_output(self, ret, target_lang):
        # map columns
        default_lang_cls = CL_MAP[DEFAULT_LANG]
        target_lang_cls = CL_MAP[target_lang]
        for idx, cl in enumerate(target_lang_cls):
            if ret[cl]:
                ret[default_lang_cls[idx]] = ret[cl]

        # remove unuse columns
        unuse_cls = []
        for lang in SUPPORT_LANG:
            unuse_cls = unuse_cls + CL_MAP[lang]

        for cl in unuse_cls:
            if cl in ret:
                ret.pop(cl)

        return ret


class BlogCUSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = '__all__'
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


class MyBlogSerializer(BlogSerializer):

    class Meta:
        model = Blog
        fields = [
            'id',
            'created_at',
            'status_type',
            'is_valid',
            'author',
            'author_info',
            'related_blog',
            'thumbnail_image_url',
            'description',
            'html_string',
            'name',
            'sub_title',
            'view_count',
            'like_count',
            'replies'
        ]
        read_only_fields = ('created_at', 'created_by')


class BlogUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['status_type']

    def update(self, instance: Blog, validated_data):

        if not self.context['request'].user == instance.created_by:
            error = {'data': 'you do not have permission'}
            raise serializers.ValidationError(error)

        return super().update(instance, validated_data)
