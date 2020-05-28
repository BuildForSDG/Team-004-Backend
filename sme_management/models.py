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
    business_plan = models.TextField()
    investment_tenure_end_date = models.DateField()
    documents = models.FileField(upload_to='projects/', blank=True)
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
    COMPLETION_STATUSES = (
        ("COMPLETED", "COMPLETED"),
        ("IN_PROGRESS", "IN_PROGRESS"),
        ("UNAPPROVED", "UNAPPROVED")
    )
    project_completion_status = models.CharField(
        max_length=255,
        choices=COMPLETION_STATUSES,
        default="UNAPPROVED"
    )


class SMEProjectMilestones(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    sme_project = models.ForeignKey(
        SMEProject,
        on_delete=models.CASCADE
    )
