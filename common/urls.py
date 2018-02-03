# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import CommonConfig
from . import views

app_name = CommonConfig.name

urlpatterns = [
    url(r'^datatable/$', views.view_datatable, name='datatable'),
]


