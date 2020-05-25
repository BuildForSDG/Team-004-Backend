from django.contrib import admin
from investor_management import models

# Register your models here.
admin.site.register(models.InvestorOrganization)
admin.site.register(models.InvestorUser)
