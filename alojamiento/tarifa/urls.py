# -*- coding: utf-8 -*-
from django.conf.urls import url
from apps import TarifaConfig
from . import views

app_name = TarifaConfig.name


urlpatterns = [
    #Temporadas
    url(r'^lista_temporadas/$', views.view_lista_temporada, name='lista-temporada'),
    url(r'^lista_temporadas_json/$', views.json_lista_temporada, name='lista-temporada-json'),
    #TemporadaFecha
    url(r'^lista_temporadasfecha_json/$', views.json_lista_temporadafecha, name='lista-temporadafecha-json'),
    #Tarifa
    url(r'^lista_tarifa/$', views.view_lista_tarifa, name='lista-tarifa'),
    url(r'^lista_tarifa_json/$', views.json_lista_tarifa, name='lista-tarifa-json'),
    url(r'^obtener_tarifas_json/$', views.json_obtener_tarifas, name='obtener-tarifas-json'),
]