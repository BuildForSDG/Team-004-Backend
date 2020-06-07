from django.urls import path

from rest_framework.routers import DefaultRouter

from backoffice_management import views

router = DefaultRouter()

app_name = 'backoffice_management'

urlpatterns = [
    path('user/create/', views.CreateBackofficeUserView.as_view(),
         name='backoffice_user_create'),
    path('user/manage/<int:id>', views.ManageBackofficeUserView.as_view(),
         name='backoffice_user_manage')
]
