from django.db import models
from django.utils.translation import gettext as _


class FinancingAudit(models.Model):
    sender_name = models.CharField(
        _('Sender Name'),
        max_length=255
    )
    recipient_name = models.CharField(
        _('Recipient Name'),
        max_length=255
    )
    transaction_date = models.DateTimeField(
        _('Transaction Date'),
        auto_now_add=True
    )
    TRANSACTION_TYPE = (
        ("DISBURSEMENT", "DISBURSEMENT"),
        ("INVESTMENT", "INVESTMENT"),
    )
    transaction_type = models.CharField(
        max_length=255,
        choices=TRANSACTION_TYPE,
        default="OTHER"
    )
