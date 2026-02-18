"""
====================================================
MULTISHOP - Main URL Configuration
====================================================
All website URLs are controlled from here
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # ❌ OLD: include('products.urls') ← was wrong name
    # ✅ NEW: include('store.urls')    ← correct app name
    path('', include('store.urls')),
]

# Serve media & static files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)