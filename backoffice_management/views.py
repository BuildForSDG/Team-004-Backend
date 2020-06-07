from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from backoffice_management.serializers import *


class CreateBackofficeUserView(generics.CreateAPIView):
    """Create a Backoffice User in the system"""
    serializer_class = CreateBackOfficeUserSerializer
    queryset = BackofficeUser.objects.all()


class ManageBackofficeUserView(generics.RetrieveUpdateAPIView):
    """Manage Backoffice User in the database"""

    queryset = BackofficeUser.objects.all()
    serializer_class = ManageBackofficeUserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Retrieve the Backoffice User for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
