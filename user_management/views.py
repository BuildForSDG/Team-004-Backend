from django.contrib.auth import get_user_model

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics, authentication, permissions

from user_management.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class AuthenticateUserView(ObtainAuthToken):
    """Create a new authentication for user"""
    serializer_class = AuthTokenSerializer
    # user = serializer_class.validated_data['user']
    # token, created = Token.objects.get_or_create(user=user)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated users."""
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user