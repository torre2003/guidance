# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from . import templates_pdf
from framework import ManagerLog, ManagerCliente, ManagerPotencialCliente


@login_required
def json_log(request):
    print request.POST.get('modelo')
    print request.POST.get('modelo_id')
    modelo = request.POST.get('modelo')
    modelo_id = request.POST.get('modelo_id')
    titulo = None
    objeto = None
    try:
        if modelo == 'cliente':
            objeto = ManagerCliente.obtener_cliente(int(modelo_id))
            titulo = objeto.nombres
        elif modelo == 'potencial_cliente':
            objeto = ManagerPotencialCliente.obtener_potencial_cliente(int(modelo_id))
            titulo = objeto.nombre_completo
        else:
            raise Exception('Modelo invalido')
    except Exception, e:
        print e
        return JsonResponse({
            'state':'error',
            'messages':[{'type': 'Error', 'text': 'Petición corrupta'}]
        })
    logs = ManagerLog.obtener_logs(tipo_modelo=type(objeto),modelo_id=modelo_id).select_related('user')
    respuesta = {}
    columnas = []
    columnas.append({'title':'Id', 'data':'id'});
    columnas.append({'title':'Usuario', 'data':'user', });
    columnas.append({'title':'Fecha', 'data':'fecha',  });
    columnas.append({'title':'Información', 'data':'info',  "width": "400px"});
    data_table = []
    for item in logs:
        aux = {}
        aux['id'] = item.id
        aux['user'] = unicode(item.user.username)
        aux['fecha'] = unicode(item.fecha)
        aux['info'] = ''
        info = item.info
        for key_info in info:
            aux['info'] += unicode(key_info) + ': '+ unicode(info[key_info]) +' <br /> '
        data_table.append(aux)
    # data_table = [{
    #     'id':1,
    #     'user':1,
    #     'fecha':1,
    #     'info':'asdadsasd'
    # }]
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    respuesta['state'] = 'success'
    respuesta['messages'] = [{'type': '', 'text': ''}]
    return JsonResponse(respuesta)
"""
    return JsonResponse({
        'state':'error',
        'messages':[{'type': 'Error', 'text': 'Problemas con potencial cliente.'}]
    })
"""