"""lyceum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from lyceum import settings

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('catalog/', include('catalog.urls'), name='catalog'),
    path('about/', include('about.urls'), name='about'),
    path('auth/', include('users.urls'), name='auth'),
    path('auth/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include('homepage.urls'), name='homepage'),
]

if settings.DEBUG:
    urlpatterns = [
                      path('__debug__/', include('debug_toolbar.urls')),
                  ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
