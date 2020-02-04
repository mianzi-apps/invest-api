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
    re_path('api/(?P<version>(v1|v2))/', include('authentication.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('farms.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('structures.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('wallet.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('projects.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('transactions.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('animals.urls')),
    re_path('api/(?P<version>(v1|v2))/', include('plants.urls')),
]
