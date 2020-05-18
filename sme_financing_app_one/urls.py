from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sme_financing_app_one import views


router = DefaultRouter()
router.register('v1/profile', views.ProfileViewSet)
router.register('v1/sme', views.SMEViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
