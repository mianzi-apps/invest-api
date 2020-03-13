"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.urls import include, re_path, path
from django.contrib import admin
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.authentication.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.farms.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.structures.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.wallet.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.projects.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.transactions.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.animals.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.plants.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('api.apps.notifications.urls')),
]
