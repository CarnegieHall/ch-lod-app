"""chlod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.urls import re_path


from . import views

urlpatterns = [
    re_path(r'^$', views.route_homepage),
    re_path(r'^works/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_works),
    re_path(r'^works/(?P<id>[0-9]+)', views.route_works),
    re_path(r'^events/(?P<id>[0-9]+)/work_(?P<product_id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_products),
    re_path(r'^events/(?P<id>[0-9]+)/work_(?P<product_id>[0-9]+)', views.route_products),
    re_path(r'^events/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_events),
    re_path(r'^events/(?P<id>[0-9]+)', views.route_events),
    re_path(r'^venues/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_venues),
    re_path(r'^venues/(?P<id>[0-9]+)', views.route_venues),
    re_path(r'^names/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_names),
    re_path(r'^names/(?P<id>[0-9]+)', views.route_names),
    re_path(r'^instruments/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_instruments),
    re_path(r'^instruments/(?P<id>[0-9]+)', views.route_instruments),
    re_path(r'^roles/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_roles),
    re_path(r'^roles/(?P<id>[0-9]+)', views.route_roles),
    re_path(r'^ensembles/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_ensembles),
    re_path(r'^ensembles/(?P<id>[0-9]+)', views.route_ensembles),
    re_path(r'^genres/(?P<id>[0-9]+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_genres),
    re_path(r'^genres/(?P<id>[0-9]+)', views.route_genres),
    # re_path(r'^sparql/select', views.route_sparql_query),
    re_path(r'^sparql/', views.route_sparql),
    re_path(r'^void/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_void),
    re_path(r'^void/', views.route_void),
    re_path(r'^vocabulary/roles/$', views.route_vocab_role),
    re_path(r'^vocabulary/roles/(?P<type>about|xml|turtle|jsonld|nt|n3)$', views.about_vocab_role),
    re_path(r'^vocabulary/roles/(?P<id>(?!(about|xml|turtle|jsonld|nt|n3))\w+)/(?P<type>about|xml|turtle|jsonld|nt|n3)', views.about_vocab_roles),
    re_path(r'^vocabulary/roles/(?P<id>(?!(about|xml|turtle|jsonld|nt|n3))\w+)', views.route_vocab_roles),
    re_path(r'^model/Entity', views.about_model_entity),
    re_path(r'^model/WorkPerformance', views.about_model_workperformance)
]
