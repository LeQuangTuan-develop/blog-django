from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])  # type: ignore
        return Response(data, status=status.HTTP_200_OK)
