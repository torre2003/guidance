# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from apps import AlojamientoConfig
from framework import ManagerAlojamiento, ManagerCanalVenta


@login_required
def view_lista_alojamiento(request):
    context = {}
    return render(request, AlojamientoConfig.name+'/lista_alojamiento.html', context)


@login_required
def json_lista_alojamiento(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Código', 'data':'codigo'});
    columnas.append({'title':'Tipo', 'data':'tipo'});
    columnas.append({'title':'Habilitado', 'data':'habilitado'});
    alojamientos = ManagerAlojamiento.obtener_alojamientos()
    alojamientos.select_related('tipoalojamiento')
    data_table = []
    for item in alojamientos:
        aux = {}
        aux['id'] = unicode(item.id)
        aux['nombre'] = item.nombre
        aux['codigo'] = item.codigo
        aux['tipo'] = item.tipoalojamiento.nombre
        aux['habilitado'] = '<i class="material-icons text-green">check</i>'
        if not item.habilitado:
            aux['habilitado'] = '<i class="material-icons text-red">clear</i>'
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def json_lista_tipoalojamiento(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});
    columnas.append({'title':'Capacidad', 'data':'capacidad'});
    columnas.append({'title':'Habilitado', 'data':'habilitado'});
    tipos = ManagerAlojamiento.obtener_tiposalojamiento()
    data_table = []
    for item in tipos:
        print item
        aux = {}
        aux['id'] = item.id
        aux['nombre'] = item.nombre
        aux['descripcion'] = item.descripcion
        aux['capacidad'] = item.capacidad
        aux['habilitado'] = '<i class="material-icons text-green">check</i>'
        if not item.habilitado:
            aux['habilitado'] = '<i class="material-icons text-red">clear</i>'
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def view_lista_canalventa(request):
    context = {}
    return render(request, AlojamientoConfig.name+'/lista_canalventa.html', context)


@login_required
def json_lista_canalventa(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});
    columnas.append({'title':'Habilitado', 'data':'_habilitado'});
    canales = ManagerCanalVenta.obtener_canalesventa()
    data_table = []
    for item in canales:
        aux = {}
        aux['id'] = unicode(item.id)
        aux['nombre'] = item.nombre
        aux['descripcion'] = item.descripcion
        aux['habilitado'] = item.habilitado
        aux['_habilitado'] = '<i class="material-icons text-green">check</i>'
        if not item.habilitado:
            aux['_habilitado'] = '<i class="material-icons text-red">clear</i>'
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def json_obtener_canalesventa(request):
    canales = ManagerCanalVenta.obtener_canalesventa()
    aux_canales = []
    for canal in canales:
        aux = canal.__dict__
        aux['_state']=''
        aux_canales.append(aux)
    respuesta = {
        'state':'success',
        'canales':aux_canales,
    }
    return JsonResponse(respuesta, safe=False)
