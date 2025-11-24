"""
URL Configuration for TrikonED project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core app (landing page, etc.)
    path('', include('core.urls')),
    
    # Universities app
    path('universities/', include('universities.urls')),
    
    # Programs app
    path('programs/', include('programs.urls')),
    
    # Students app (auth, dashboard, profile)
    path('', include('students.urls')),
    
    # Applications app
    path('apply/', include('applications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "TrikonED Administration"
admin.site.site_title = "TrikonED Admin"
admin.site.index_title = "Welcome to TrikonED Admin Portal"
