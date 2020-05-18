from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication



from sme_financing_app_one import serializers
from sme_financing_app_one import models
from sme_financing_app_one import permissions

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.UserProfile.objects.all()
    filter_backends = (filters.SearchFilter,)
    authentication_classes = (TokenAuthentication,)
    search_fields = ('first_name', 'last_name', 'email',)
    permission_classes = (permissions.UpdateOwnProfile,)

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens."""
    
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES