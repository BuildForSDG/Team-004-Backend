from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user_management.urls')),
    path('api/v1/sme/', include('sme_management.urls')),
    path('api/v1/investor/', include('investor_management.urls')),
    path('api/v1/audit/', include('audit_management.urls')),
    path('api/v1/backoffice/', include('backoffice_management.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
