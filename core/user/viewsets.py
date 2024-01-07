# core/user/viewsets.py
from django.http import StreamingHttpResponse
from core.user.models import UserProfile, User
from core.user.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, mixins, generics
from rest_framework.response import Response
import requests

# Create your views here.
test_per = permissions.AllowAny
prod_per = permissions.IsAuthenticatedOrReadOnly
per_here = test_per


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)


class CurrentUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            return UserProfileSerializer

        return CUUserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = UserProfile.objects.get(base_user=request.user)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)

    def list(self, request):
        request_user = User.objects.get(pk=request.user.pk)
        # check if exsited
        if not UserProfile.objects.filter(base_user=request.user).exists():
            print('dont have profile, create!')
            UserProfile.objects.create(base_user=request_user)

        queryset = UserProfile.objects.get(base_user=request.user)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # MEMO:
        # lookup_field is the field used to filter the queryset
        # kwargs is the dict of url params
        # self.kwargs is the dict of url params
        # self.kwargs['base_user__pk'] is the value of url params
        # self.kwargs['base_user__pk'] = request.user.pk

        # check if exsited
        self.lookup_field = 'base_user__pk'
        self.kwargs['base_user__pk'] = request.user.pk
        self.queryset = UserProfile.objects.all()
        return super().update(request, *args, **kwargs)


def url2yield(url, chunksize=1024):
    s = requests.Session()
    # Note: here i enabled the streaming
    response = s.get(url, stream=True)

    chunk = True
    while chunk:
        chunk = response.raw.read(chunksize)
        if not chunk:
            break
        yield chunk


class UserProfileImageViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        queryset = UserProfile.objects.get(base_user__pk=kwargs['pk'])
        avatar_url = UserProfileSerializer(queryset).data.get('avatar')

        return StreamingHttpResponse(url2yield(avatar_url), content_type="image/png")
