from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from sme_management.serializers import *


class CreateSMEUserView(generics.CreateAPIView):
    """Create a SME user in the system"""
    serializer_class = CreateSMEUserSerializer
    queryset = SMEUser.objects.all()


class ManageSMEUserView(generics.RetrieveUpdateAPIView):
    """Manage SME Users in the database"""

    queryset = SMEUser.objects.all()
    serializer_class = ManageSMEUserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Retrieve the SMEUser for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
