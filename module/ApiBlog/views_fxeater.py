from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets, mixins

from .models import *
from .serializers_blog import *
from .serializers_series import *

from rest_framework import viewsets
from rest_framework import permissions

from rest_framework import status
from rest_framework.response import Response

from module.constant import *

# Create your views here.
test_per = permissions.AllowAny
prod_per = permissions.IsAuthenticatedOrReadOnly
per_here = test_per


class BlogViewset(viewsets.ModelViewSet):
    queryset = Blog.objects.filter(
        is_valid=1, status_type=2, domain=DOMAIN_FXEATER).order_by('-id')
    serializer_class = BlogSerializer
    permission_classes = [prod_per]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BlogSerializer

        return BlogCUSerializer

    # With cookie: cache requested url for each user for 5 minute
    @method_decorator(cache_page(10))
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count", ))
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(10))  # cache 3minute
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


class BlogHomeViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Blog.objects.filter(
        is_valid=1, status_type=2, domain=DOMAIN_FXEATER).order_by('-id')[:3]
    serializer_class = BlogSerializer
    permission_classes = [prod_per]

    @method_decorator(cache_page(10))  # cache 3minute
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BlogLikeCountViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Blog.objects.filter(
        is_valid=1, domain=DOMAIN_FXEATER).order_by('-created_at')
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.like_count = obj.like_count + 1
        obj.save(update_fields=("like_count", ))
        return super().retrieve(request, *args, **kwargs)


class ReplyViewset(viewsets.ModelViewSet):
    queryset = ReplyBlog.objects.all().order_by('-created_at')
    serializer_class = GetReplyBlogSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_superuser:  # type: ignore
            return ReplyBlog.objects.filter(created_by=self.request.user, is_valid=1).order_by('-created_at')
        return ReplyBlog.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return GetReplyBlogSerializer

        self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return PostUpdateReplyBlogSerializer

    def destroy(self, request, *args, **kwargs):
        # check if request user is admin or author
        request_user = request.user
        target_reply = ReplyBlog.objects.get(id=kwargs['pk'])
        if target_reply.created_by == request_user or request_user.is_superuser:
            target_reply.is_valid = 0
            target_reply.save()

            return Response(data='delete success')
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class SeriesViewset(viewsets.ModelViewSet):
    serializer_class = SeriesSerializer
    permission_classes = [prod_per]

    def get_queryset(self):
        # user = self.request.user

        # if not user.is_superuser:  # type: ignore
        #     return BlogSeries.objects.filter(created_by=self.request.user, is_valid=1, domain=DOMAIN_FXEATER).order_by('-created_at')
        return BlogSeries.objects.filter(is_valid=1, domain=DOMAIN_FXEATER).order_by('-created_at')

    def get_serializer_class(self):
        user = self.request.user

        if self.action == 'list' or self.action == 'retrieve' or not user.is_superuser:  # type: ignore
            return SeriesSerializer

        return SeriesCUSerializer

    def destroy(self, request, *args, **kwargs):
        # check if request user is admin or author
        request_user = request.user
        target_series = BlogSeries.objects.get(id=kwargs['pk'])
        if target_series.created_by == request_user or request_user.is_superuser:
            target_series.is_valid = 0
            target_series.save()

            return Response(data='delete success')
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        request_user = request.user
        target_series = BlogSeries.objects.get(id=kwargs['pk'])
        if target_series.created_by == request_user or request_user.is_superuser:
            return super().update(request, *args, **kwargs)
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        request_user = request.user
        if request_user.is_superuser:
            return super().create(request, *args, **kwargs)
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class MyBlogViewset(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        return Blog.objects.filter(created_by=user, domain=DOMAIN_FXEATER).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return MyBlogSerializer

        return BlogCUSerializer

    def destroy(self, request, *args, **kwargs):
        # check if request user is admin or author
        request_user = request.user
        target_blog = Blog.objects.get(id=kwargs['pk'])
        if target_blog.created_by == request_user or request_user.is_superuser:
            target_blog.is_valid = 0
            target_blog.save()

            return Response(data='delete success')
        return Response({'data': 'you do not have permission'}, status=status.HTTP_403_FORBIDDEN)


class UpdateBlogStatusViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):

        user = self.request.user
        return Blog.objects.filter(created_by=user, domain=DOMAIN_FXEATER).order_by('-created_at')

    def get_serializer_class(self):

        return BlogUpdateStatusSerializer
