# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from . import templates_pdf
from . import framework as f_cliente
from apps import ClienteConfig


@login_required
def agregar_view(request):
    context = {}
    return render(request, ClienteConfig.name+'/agregar.html', context)

@login_required
def gestion_cliente_json_view(request):
    context = {}
    if request.method == 'POST':
        post_dic = json.loads(request.POST.get('datos'))
        print post_dic
        res_json = {}
        if post_dic['opcion'] == 'CONSULTA':
            cliente = f_cliente.obtener_cliente(post_dic['cliente'])
            dic_cliente = cliente.__dict__
            fecha_nacimiento = str(dic_cliente['fecha_nacimiento'].day)+'-'+str(dic_cliente['fecha_nacimiento'].month)+'-'+str(dic_cliente['fecha_nacimiento'].year)
            dic_cliente['fecha_nacimiento'] = fecha_nacimiento
            dic_cliente['_state'] = ''
            if cliente is None:
                return JsonResponse({
                    'state':'error',
                    'messages':[{'type': 'Error', 'text': 'Petición corrupta, El cliente no existe!'}]
                })
            return JsonResponse({
                    'state':'success',
                    'messages':[],
                    'cliente':dic_cliente,
                })
        if post_dic['opcion'] == 'NUEVO':
            info_cliente = post_dic['data']
            fecha_nacimiento = None
            if info_cliente['fecha_nacimiento'] != '':
                try:
                    fecha_nacimiento = datetime.date(datetime.strptime(info_cliente['fecha_nacimiento'], "%d-%m-%Y"))
                except Exception, e:
                    print '',e
            nuevo_cliente = f_cliente.crear_cliente (
                nombres = info_cliente['nombres'],
                apellidos = info_cliente['apellidos'],
                direccion = info_cliente['direccion'],
                ciudad = info_cliente['ciudad'],
                fecha_nacimiento = fecha_nacimiento,
                pais = info_cliente['pais'],
                email = info_cliente['email'],
                sexo = info_cliente['gender'],
                telefono = info_cliente['telefono'],
                rut = info_cliente['rut'],
                digito_verificador = info_cliente['dv'],
                descripcion = info_cliente['descripcion'],
            )
            state='success'
            messages=[]
            if nuevo_cliente is None:
                state='error'
                messages.append({'type': 'Error', 'text': 'El cliente ya ha sido creado'})
                print ''
            return JsonResponse({
                'state':state,
                'messages':messages,
            })
        if post_dic['opcion'] == 'EDICION':
            info_cliente = post_dic['data']
            cliente = f_cliente.obtener_cliente(info_cliente['id'])
            if cliente is None or not( cliente.rut == info_cliente['rut'] and cliente.digito_verificador == info_cliente['dv']):
                return JsonResponse({
                    'state':'error',
                    'messages':[{'type': 'Error', 'text': 'Petición corrupta'}]
                })
            fecha_nacimiento = None
            if info_cliente['fecha_nacimiento'] != '':
                try:
                    fecha_nacimiento = datetime.date(datetime.strptime(info_cliente['fecha_nacimiento'], "%d-%m-%Y"))
                except Exception, e:
                    print '',e
            cliente = f_cliente.editar_cliente (
                cliente_id = info_cliente['id'],
                nombres = info_cliente['nombres'],
                apellidos = info_cliente['apellidos'],
                direccion = info_cliente['direccion'],
                ciudad = info_cliente['ciudad'],
                fecha_nacimiento = fecha_nacimiento,
                pais = info_cliente['pais'],
                email = info_cliente['email'],
                sexo = info_cliente['gender'],
                telefono = info_cliente['telefono'],
                descripcion = info_cliente['descripcion'],
            )
            return JsonResponse({
                'state':'success',
                'messages':[]
            })
    return JsonResponse({
        'state':'error',
        'messages':[{'type': 'Error', 'text': 'Problemas al crear el cliente'}]
    })

@login_required
def lista_view(request):
    context = {}
    context['clientes'] = f_cliente.obtener_clientes()
    return render(request, ClienteConfig.name+'/lista.html', context)

@login_required
def json_pdf_ficha_ingreso(request):
    if request.method == 'POST':
    #if True:
        content = None
        styles=None
        images=None
        if request.POST.has_key('cliente'):
            cliente = f_cliente.obtener_cliente(request.POST.get('cliente'))
            full_name = cliente.nombres+' '+cliente.apellidos
            rut = str(cliente.rut)+'-'+str(cliente.digito_verificador)
            content, styles, images = templates_pdf.ficha_ingreso(
                nombre=full_name,
                rut=rut, 
                direccion=cliente.direccion, 
                ciudad=cliente.ciudad, 
                email=cliente.email, 
                telefono=cliente.telefono,
            )
        else:
            content, styles, images = templates_pdf.ficha_ingreso()
        return JsonResponse({
            'state':'success',
            'content': content,
            'styles': styles,
            'images': images,
            'messages':['Mensaje'],
        })
    return JsonResponse({
        'state':'error',
        'messages':[{'type': 'Error', 'text': 'Petición corrupta'}]
    })
