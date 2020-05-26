from django.db import models
from django.conf import settings
from sme_management.models import SMEProject


class InvestorOrganization(models.Model):
    org_name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return '%s at %s' % (self.org_name, self.address)


class InvestorUser(models.Model):
    investor_org = models.OneToOneField(InvestorOrganization, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class InvestorOrgSMEProjectInvestments(models.Model):
    """Model used to store how much an investor paid for a project"""
    investor_org = models.ManyToManyField(InvestorOrganization)
    sme_project = models.ManyToManyField(SMEProject)
    amount_invested = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
