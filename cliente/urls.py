# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import ClienteConfig
from . import views

app_name = ClienteConfig.name

urlpatterns = [
    url(r'^agregar/$', views.agregar_view, name='agregar'),
    url(r'^gestion_json/$', views.gestion_cliente_json_view, name='gestion-json'),
    url(r'^lista/$', views.lista_view, name='lista'),
]


