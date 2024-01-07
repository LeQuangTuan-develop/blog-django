from rest_framework import serializers
from .models import *


class SeriesSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source="created_by.username")
    author_info = serializers.SerializerMethodField()
    blogs = serializers.SerializerMethodField()

    def get_author_info(self, obj):
        return {
            "author_id": obj.created_by.id,
            "avatar": obj.created_by.profile.avatar.url,
        }

    def get_blogs(self, obj: BlogSeries):
        blog_obj = Blog.objects.filter(series=obj, is_valid=1, status_type=2)
        out_data = []
        if blog_obj:
            for _b in blog_obj:
                out_data.append({
                    'id': _b.pk,
                    'name': _b.name,
                })
        return out_data

    class Meta:
        model = BlogSeries
        fields = [
            'id',
            'name',
            'blogs',
            'created_at',
            'author',
            'author_info',
            'description',
        ]
        read_only_fields = ('created_at', 'created_by')


class SeriesCUSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogSeries
        fields = '__all__'
        read_only_fields = ('created_at', 'created_by', 'is_valid')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user

        new_series = BlogSeries.objects.create(**validated_data)

        return new_series
