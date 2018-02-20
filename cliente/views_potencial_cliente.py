# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from . import templates_pdf
from framework import ManagerPotencialCliente
from apps import ClienteConfig


@login_required
def view_lista_potencial_cliente(request):
    context = {}
    return render(request, ClienteConfig.name+'/lista_potenciales_clientes.html', context)


@login_required
def json_lista_potencial_cliente(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'Id', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre_completo'});
    columnas.append({'title':'Email', 'data':'email'});
    columnas.append({'title':'Teléfono', 'data':'telefono'});
    columnas.append({'title':'Nacionalidad', 'data':'nacionalidad'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});
    columnas.append({'title':'Acciones', 'data':'acciones'});

    clientes = ManagerPotencialCliente.obtener_potenciales_clientes()
    data_table = []
    for item in clientes:
        aux = {}
        aux['id'] = item.id
        aux['nombre_completo'] = item.nombre_completo
        aux['email'] = item.email
        aux['telefono'] = unicode(item.telefono)
        aux['nacionalidad'] = item.nacionalidad
        aux['descripcion'] = item.descripcion
        aux['acciones'] = '<table  style ="width:100%; border:0px; padding:0px;"><tbody><tr><td style="width:50px; border:0px; padding:0px;"><button name="log" potencial_cliente="'+unicode(item.id)+'" class="btn btn-default nav-pill waves-effect waves-block toggled"><i class="material-icons">info</i></button></td><td style="width:50%; border:0px; padding:0px;"><button name="editar"   potencial_cliente="'+unicode(item.id)+'" class="btn btn-default nav-pill waves-effect waves-block toggled" ><i class="material-icons">edit</i></button></td></tr></tbody></table>'
        data_table.append(aux)

    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)



@login_required
def json_gestion_potencial_cliente(request):
    context = {}
    if request.method == 'POST':
        post_dic = json.loads(request.POST.get('datos'))
        print post_dic
        res_json = {}
        if post_dic['opcion'] == 'CONSULTA':
            potencial_cliente = ManagerPotencialCliente.obtener_potencial_cliente(post_dic['potencial_cliente'])
            dic_potencial_cliente = potencial_cliente.__dict__
            dic_potencial_cliente['fecha'] = ''
            dic_potencial_cliente['_state'] = ''
            if potencial_cliente is None:
                return JsonResponse({
                    'state':'error',
                    'messages':[{'type': 'Error', 'text': 'Petición corrupta, El potencial cliente no existe!'}]
                })
            return JsonResponse({
                    'state':'success',
                    'messages':[],
                    'potencial_cliente':dic_potencial_cliente,
                })
        if post_dic['opcion'] == 'NUEVO':
            info_potencial_cliente = post_dic['data']
            nuevo_potencial_cliente = ManagerPotencialCliente.crear_potencial_cliente (
                nombre_completo = info_potencial_cliente['nombre_completo'],
                email = info_potencial_cliente['email'] if info_potencial_cliente['email'] != '' else '',
                telefono = info_potencial_cliente['telefono'],
                nacionalidad = info_potencial_cliente['nacionalidad'],
                descripcion = info_potencial_cliente['descripcion'],
                user_id = request.user.id,
            )
            state='success'
            messages=[]
            return JsonResponse({
                'state':state,
                'messages':messages,
            })
        if post_dic['opcion'] == 'EDICION':
            info_potencial_cliente = post_dic['data']
            print info_potencial_cliente
            potencial_cliente = ManagerPotencialCliente.obtener_potencial_cliente(info_potencial_cliente['id'])
            if potencial_cliente is None:
                return JsonResponse({
                    'state':'error',
                    'messages':[{'type': 'Error', 'text': 'Petición corrupta no se encuentra el potencal cliente.'}]
                })
            potencial_cliente = ManagerPotencialCliente.editar_potencial_cliente (
                potencial_cliente_id=info_potencial_cliente['id'],
                nombre_completo=info_potencial_cliente['nombre_completo'],
                email=info_potencial_cliente['email'],
                telefono=info_potencial_cliente['telefono'],
                nacionalidad=info_potencial_cliente['nacionalidad'],
                descripcion=info_potencial_cliente['descripcion'],
                user_id=request.user.id,
            )
            return JsonResponse({
                'state':'success',
                'messages':[]
            })
            
    return JsonResponse({
        'state':'error',
        'messages':[{'type': 'Error', 'text': 'Problemas con potencial cliente.'}]
    })