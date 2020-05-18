from django.contrib import admin
from sme_financing_app_one import models
# Register your models here.

admin.site.register(models.UserProfile)
admin.site.register(models.SME)
admin.site.register(models.SMEUser)
admin.site.register(models.SMEProject)