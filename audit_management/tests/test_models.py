from django.test import TestCase
from audit_management.models import FinancingAudit


class FinancingAuditModelTests(TestCase):

    def setUp(self):
        FinancingAudit.objects.create(
            sender_name="Andela", recipient_name="team-004", transaction_date="28-05-2020")

    def test_financing_audit_created(self):
        """Test that finance audit can be created"""
        finance = FinancingAudit.objects.all()

        self.assertEqual(len(finance), 1)
