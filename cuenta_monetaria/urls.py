# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import CuentaMonetariaConfig
from . import views

app_name = CuentaMonetariaConfig.name

urlpatterns = [
    # url(r'^datatable/$', views.view_datatable, name='datatable'),
    # url(r'^test_11/$', views.view_test_11, name='test-11'),
]