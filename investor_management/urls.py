from django.urls import path

from rest_framework.routers import DefaultRouter

from investor_management import views

router = DefaultRouter()

app_name = 'investor_management'

urlpatterns = [
    path('user/create/', views.CreateInvestorUserView.as_view(), name='investor_user_create'),
    path('user/manage/<int:id>', views.ManageInvestorUserView.as_view(), name='investor_user_manage')
]
