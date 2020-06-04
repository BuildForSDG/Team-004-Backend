from django.urls import path, include

from rest_framework.routers import DefaultRouter

from sme_management import views

router = DefaultRouter()
router.register('project/milestones', views.SMEProjectMilestoneViewSet)

app_name = 'sme_management'

urlpatterns = [
    path('user/create/', views.CreateSMEUserView.as_view(), name='sme_user_create'),
    path('user/manage/<int:id>', views.ManageSMEUserView.as_view(), name='sme_user_manage'),
    path('project', views.SMEProjectAPIView.as_view(), name='sme_project_create'),
    path('project/milestones/<int:id>', views.SMEProjectMilestoneAPIView.as_view(), name='sme_project_milestone'),
    path('project/all', views.SMEProjectsListAPIView.as_view(), name='sme_project_timeline'),
    path('', include(router.urls))
]
