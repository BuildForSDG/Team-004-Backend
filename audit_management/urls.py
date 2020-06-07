from django.urls import path
from rest_framework.routers import DefaultRouter

from audit_management import views

router = DefaultRouter()

app_name = 'audit_management'

urlpatterns = [
    path('', views.ListFinancingAuditView.as_view(), name='finance_audit_list')
]
