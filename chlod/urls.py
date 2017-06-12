"""chlod URL Configuration

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
from django.conf.urls import url
from django.contrib import admin


from . import views

urlpatterns = [
    url(r'^$', views.route_homepage),
    url(r'^works/(?P<id>[0-9]+)/about', views.about_works),
    url(r'^works/(?P<id>[0-9]+)', views.route_works),
    url(r'^events/(?P<id>[0-9]+)/about', views.about_events),
    url(r'^events/(?P<id>[0-9]+)', views.route_events),
    url(r'^sparql/select', views.route_sparql_query),    
    url(r'^sparql/', views.route_sparql)    


]
