# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from apps import AlojamientoConfig
from . import views, views_reservaalojamiento

app_name = AlojamientoConfig.name



urlpatterns = [
    
    #Alojamiento
    url(r'^lista_alojamiento/$', views.view_lista_alojamiento, name='lista-alojamiento'),
    url(r'^lista_alojamiento_json/$', views.json_lista_alojamiento, name='lista-alojamiento-json'),
    url(r'^lista_tipoalojamiento_json/$', views.json_lista_tipoalojamiento, name='lista-tipoalojamiento-json'),
    #Tarifa
    url(r'^tarifa/', include('alojamiento.tarifa.urls')),
    #Canal Venta
    url(r'^lista_canalventa/$', views.view_lista_canalventa, name='lista-canalventa'),
    url(r'^lista_canalventa_json/$', views.json_lista_canalventa, name='lista-canalventa-json'),
    url(r'^obtener_canalesventa_json/$', views.json_obtener_canalesventa, name='obtener-canalesventa-json'),
    #Reserva alojamiento
    url(r'^lista_reservaalojamiento/$', views_reservaalojamiento.view_lista_reservaalojamiento, name='lista-reservaalojamiento'),
    url(r'^lista_comentario_json/$', views_reservaalojamiento.json_lista_comentario, name='lista-comentario-json'),
    url(r'^data_ocupacionalojamiento/$', views_reservaalojamiento.json_data_ocupacionalojamiento, name='data-ocupacionalojamiento-json'),
    url(r'^comprobarocupacion_json/$', views_reservaalojamiento.json_comprobarocupacion, name='comprobarocupacion-json'),
    url(r'^crear_reserva_json/$', views_reservaalojamiento.json_crear_reserva, name='crear-reserva-json'),
    
]


