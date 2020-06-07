from rest_framework import generics

from audit_management.models import FinancingAudit
from audit_management.serializers import FinancingAuditSerializer


class ListFinancingAuditView(generics.ListAPIView):
    """List the Financial Details"""
    queryset = FinancingAudit.objects.all()
    serializer_class = FinancingAuditSerializer
