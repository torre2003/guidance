# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import EmpresaConfig
from . import views

app_name = EmpresaConfig.name

urlpatterns = [
    #Empresa
    # url(r'^gestion_cliente_json/$', views.json_gestion_cliente, name='gestion-cliente-json'),
    url(r'^lista_empresa/$', views.view_lista_empresa, name='lista-empresa'),
    url(r'^lista_empresa_json/$', views.json_lista_empresa, name='lista-empresa-json'),

    url(r'^lista_clientes_asociados_empresa_json/$', views.json_lista_clientes_asociados_empresa, name='lista-clientes-asociados-empresa-json'),
]