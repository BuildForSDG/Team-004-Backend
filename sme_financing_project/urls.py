from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user_management.urls')),
    path('api/v1/sme/', include('sme_management.urls')),
    path('api/v1/investor/', include('investor_management.urls'))
]
