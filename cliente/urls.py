# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import ClienteConfig
from . import views
from . import views_potencial_cliente

app_name = ClienteConfig.name

urlpatterns = [
    #Cliente
    url(r'^agregar/$', views.view_agregar, name='agregar'),
    url(r'^gestion_cliente_json/$', views.json_gestion_cliente, name='gestion-cliente-json'),
    url(r'^lista_cliente/$', views.view_lista_cliente, name='lista-cliente'),
    url(r'^lista_cliente_json/$', views.json_lista_cliente, name='lista-cliente-json'),
    url(r'^ficha_ingreso/$', views.json_pdf_ficha_ingreso, name='ficha-ingreso'),

    #Potencial Cliente
    url(r'^lista_potencial_cliente/$', views_potencial_cliente.view_lista_potencial_cliente, name='lista-potencial-cliente'),
    url(r'^lista_potencial_cliente_json/$', views_potencial_cliente.json_lista_potencial_cliente, name='lista-potencial-cliente-json'),
    url(r'^gestion_potencial_cliente_json/$', views_potencial_cliente.json_gestion_potencial_cliente, name='gestion-potencial-cliente-json'),
    
    
]


