from django.urls import path

from rest_framework.routers import DefaultRouter

from sme_management import views

router = DefaultRouter()

app_name = 'sme_management'

urlpatterns = [
    path('user/create/', views.CreateSMEUserView.as_view(), name='sme_user_create'),
    path('user/manage/<int:id>', views.ManageSMEUserView.as_view(), name='sme_user_manage')
]
