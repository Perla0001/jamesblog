from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vlogs.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('skincare/', include('skincare.urls')),
    path('coreano/', include('coreano.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)