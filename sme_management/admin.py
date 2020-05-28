from django.contrib import admin
from sme_management import models

# Register your models here.
admin.site.register(models.SMEUser)
admin.site.register(models.SME)
admin.site.register(models.SMEProject)
admin.site.register(models.SMEProjectMilestones)
