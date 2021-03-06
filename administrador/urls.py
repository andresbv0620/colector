"""colector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from administrador.views import DevolverJson
from . import views

urlpatterns = [
   
url(r'^$', 'administrador.views.reporte'),
url(r'^devolver/json/$', DevolverJson.as_view()),
url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'administrador/auth/login.html'}),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'administrador/auth/login.html'}),
url(r'^dashboard/$', views.dashboard),
url(r'^index/$', views.index),
url(r'^test/', 'administrador.views.testview'),

    
]