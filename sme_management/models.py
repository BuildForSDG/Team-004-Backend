from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class SME(models.Model):
    org_name = models.CharField(max_length=255)
    address = models.TextField()
    documents = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return self.org_name


class SMEUser(models.Model):
    sme = models.OneToOneField(SME, on_delete=models.CASCADE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class SMEProject(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField(default='NO DESCRIPTION')
    business_plan = models.FileField(upload_to='business-plans/', default=None)
    investment_tenure_end_date = models.DateField()
    cashflow_statement = models.FileField(upload_to='cashflow-stmts/', default=None, null=True)
    income_statement = models.FileField(upload_to='income-stmts/', default=None, null=True)
    balance_sheet = models.FileField(upload_to='balance-sheets/', default=None, null=True)
    category = models.CharField(max_length=100)
    amount_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    amount_raised = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    equity_offering = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    STATUS = (
        ("COMPLETED", "COMPLETED"),
        ("IN_PROGRESS", "IN_PROGRESS"),
        ("UNAPPROVED", "UNAPPROVED")
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS,
        default="UNAPPROVED"
    )
    sme = models.ForeignKey(
        SME,
        on_delete=models.CASCADE
    )


class SMEProjectMilestones(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    sme = models.ForeignKey(
        SME,
        on_delete=models.CASCADE
    )
    sme_project = models.ForeignKey(
        SMEProject,
        on_delete=models.CASCADE
    )
    proof_of_completion = models.FileField(upload_to='milestone-complete-proof/', default=None, null=True)
    STATUS = (
        ("COMPLETED", "COMPLETED"),
        ("IN_PROGRESS", "IN_PROGRESS"),
        ("NOT_STARTED", "NOT_STARTED")
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS,
        default="NOT_STARTED"
    )
