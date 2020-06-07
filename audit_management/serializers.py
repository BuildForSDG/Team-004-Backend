from audit_management.models import FinancingAudit

from rest_framework import serializers


class FinancingAuditSerializer(serializers.ModelSerializer):
    """Serializer for Audit Finance"""

    class Meta:
        model = FinancingAudit
        fields = ('id', 'sender_name', 'recipient_name', 'transaction_date', 'transaction_type')
        read_only_fields = ('id',)
