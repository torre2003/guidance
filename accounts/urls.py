# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import AccountsConfig
from . import views

app_name = AccountsConfig.name

urlpatterns = [
    url(r'^$', views.login_view, name='login'),
    url(r'^index/$', views.index_view, name='index'),
    url(r'^logout/$', views.logout_view, name='logout'),
]