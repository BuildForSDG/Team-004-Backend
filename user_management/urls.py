from django.urls import path, include
from user_management import views

app_name = 'user_management'

urlpatterns = [
    path('login', views.AuthenticateUserView.as_view(), name='login'),
    path('all-users', views.ListUsersView.as_view(), name='all'),
    path('manage', views.ManageUserView.as_view(), name='manage'),
]
