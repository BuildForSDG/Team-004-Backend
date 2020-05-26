from django.db import models
from django.conf import settings


# Create your models here.
class BackofficeUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
