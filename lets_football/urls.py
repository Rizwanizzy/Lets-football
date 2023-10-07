
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('users/', include('user_side.urls')),
    path('admin_side/', include('admin_side.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
