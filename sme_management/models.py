from django.db import models
from django.conf import settings


class SME(models.Model):
    org_name = models.CharField(max_length=255)
    address = models.TextField()
    documents = models.FileField(upload_to='documents/', blank=True)

    def __str__(self):
        return '%s at %s' % (self.org_name, self.address)


class SMEUser(models.Model):
    sme = models.OneToOneField(SME, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class SMEProject(models.Model):
    project_name = models.CharField(max_length=255, default='No Project Name Given')
    business_plan = models.TextField()
    tenure = models.DateField()
    documents = models.FileField(upload_to='projects/', blank=True)
    category = models.CharField(max_length=100)
