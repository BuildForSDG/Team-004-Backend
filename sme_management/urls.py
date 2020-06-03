from django.urls import path, include

from rest_framework.routers import DefaultRouter

from sme_management import views

router = DefaultRouter()
router.register('user/project/milestones', views.SMEProjectMilestoneViewSet)

app_name = 'sme_management'

urlpatterns = [
    path('user/create/', views.CreateSMEUserView.as_view(), name='sme_user_create'),
    path('user/manage/<int:id>', views.ManageSMEUserView.as_view(), name='sme_user_manage'),
    path('user/project', views.SMEProjectAPIView.as_view(), name='sme_project_create'),
    path('user/project/milestones/<int:id>', views.SMEProjectMilestoneAPIView.as_view(), name='sme_project_milestone'),
    path('projects/all', views.SMEProjectsListAPIView.as_view(), name='sme_project_timeline'),
    path('', include(router.urls))
]
