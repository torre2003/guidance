# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import CommonConfig
from . import views

app_name = CommonConfig.name

urlpatterns = [
    url(r'^datatable/$', views.view_datatable, name='datatable'),
    #Testing
    url(r'^test/$', views.view_test, name='test'),
    url(r'^test_01/$', views.json_test_01, name='test-01'),
    url(r'^test_02/$', views.json_test_02, name='test-02'),
    url(r'^test_03/$', views.json_test_03, name='test-03'),
    url(r'^test_04/$', views.json_test_04, name='test-04'),
    url(r'^test_05/$', views.json_test_05, name='test-05'),
    url(r'^test_06/$', views.json_test_06, name='test-06'),
    url(r'^test_07/$', views.json_test_07, name='test-07'),
    url(r'^test_08/$', views.json_test_08, name='test-08'),
    url(r'^test_09/$', views.json_test_09, name='test-09'),

    #Vista normal
    url(r'^test_11/$', views.view_test_11, name='test-11'),
]