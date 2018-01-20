# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from . import framework as f_cliente
from apps import ClienteConfig


@login_required
def agregar_view(request):
    context = {}
    return render(request, ClienteConfig.name+'/agregar.html', context)

@login_required
def gestion_cliente_json_view(request):
    context = {}
    if request.POST:
        post_dic = json.loads(request.POST.get('datos'))
        print post_dic
        res_json = {}
        if post_dic['opcion'] == 'NUEVO':
            info_cliente = post_dic['data']
            
            fecha_nacimiento = None
            print 'aaaa ', info_cliente['fecha_nacimiento']
            if info_cliente['fecha_nacimiento'] != '':
                try:
                    print '2',datetime.strptime(info_cliente['fecha_nacimiento'], "%d-%m-%Y")
                    fecha_nacimiento = datetime.date(datetime.strptime(info_cliente['fecha_nacimiento'], "%d-%m-%Y"))
                except Exception, e:
                    print '',e
            print ('fn ',fecha_nacimiento)
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

    return JsonResponse({
        'state':'error',
        'messages':[{'type': 'Error', 'text': 'Problemas al crear el cliente'}]
    })

@login_required
def lista_view(request):
    context = {}
    context['clientes'] = f_cliente.obtener_clientes()
    return render(request, ClienteConfig.name+'/lista.html', context)
