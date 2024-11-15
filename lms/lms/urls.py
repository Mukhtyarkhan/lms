from django.contrib import admin
from django.urls import path, include
from  . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.admin_home, name='home'),
    # path('teacher/', views.teacher, name='teacher'),
    path('admin/', admin.site.urls),
    path("auth/", include('auth_app.urls')),
    path("teacher/", include('teacher.urls')),
    # path('buyer/', include('buyer.urls')),
    
    
    
    
    
    
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
