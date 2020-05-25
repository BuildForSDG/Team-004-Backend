from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, viewsets

from investor_management.serializers import *


class CreateInvestorUserView(generics.CreateAPIView):
    """Create a Investor user in the system"""
    serializer_class = CreateInvestorUserSerializer
    queryset = InvestorUser.objects.all()


class ManageInvestorUserView(generics.RetrieveUpdateAPIView):
    """Manage SME Users in the database"""

    queryset = InvestorUser.objects.all()
    serializer_class = ManageInvestorUserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Retrieve the SMEUser for the authenticated user"""
        return self.queryset.filter(user=self.request.user)
