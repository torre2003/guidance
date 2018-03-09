# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import json

from . import templates_pdf
from framework import ManagerCliente, ManagerLog
from apps import ClienteConfig


@login_required
def view_agregar(request):
    context = {}
    return render(request, ClienteConfig.name+'/agregar.html', context)


@login_required
def json_gestion_cliente(request):
    context = {}
    if request.method == 'POST':
        post_dic = json.loads(request.POST.get('datos'))
        print post_dic
        res_json = {}
        if post_dic['opcion'] == 'CONSULTA':
            cliente = ManagerCliente.obtener_cliente(post_dic['cliente'])
            dic_cliente = cliente.__dict__
            fecha_nacimiento = ''
            if dic_cliente['fecha_nacimiento'] is not None:
                fecha_nacimiento = unicode(dic_cliente['fecha_nacimiento'].day)+'-'+unicode(dic_cliente['fecha_nacimiento'].month)+'-'+unicode(dic_cliente['fecha_nacimiento'].year)
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
            nuevo_cliente = ManagerCliente.crear_cliente (
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
                user_id=request.user.id,
            )
            state='success'
            cliente_id = None
            messages=[]
            if nuevo_cliente is None:
                state='error'
                messages.append({'type': 'Error', 'text': 'El cliente ya ha sido creado'})
            else:
                cliente_id = nuevo_cliente.id
            return JsonResponse({
                'state':state,
                'messages':messages,
                'cliente_id':cliente_id,
            })
        if post_dic['opcion'] == 'EDICION':
            info_cliente = post_dic['data']
            cliente = ManagerCliente.obtener_cliente(info_cliente['id'])
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
            cliente = ManagerCliente.editar_cliente (
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
                user_id = request.user.id,
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
def view_lista_cliente(request):
    context = {}
    context['imprimir_cliente'] = None
    #context['clientes'] = ManagerCliente.obtener_clientes()
    if request.GET.get('imprimir_cliente'):
        context['imprimir_cliente'] = request.GET.get('imprimir_cliente')
    return render(request, ClienteConfig.name+'/lista_clientes.html', context)


@login_required
def json_lista_cliente(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Rut', 'data':'rut'});
    columnas.append({'title':'Nombres', 'data':'nombres'});
    columnas.append({'title':'Apellidos', 'data':'apellidos'});
    columnas.append({'title':'Fecha de nacimiento', 'data':'nacimiento'});
    columnas.append({'title':'Dirección', 'data':'direccion'});
    columnas.append({'title':'Email', 'data':'email'});
    columnas.append({'title':'Teléfono', 'data':'telefono'});
    columnas.append({'title':'Acciones', 'data':'acciones'});

    clientes = ManagerCliente.obtener_clientes()
    data_table = []
    for item in clientes:
        aux = {}
        aux['id'] = item.id
        aux['rut'] = unicode(item.rut)+'-'+unicode(item.digito_verificador)
        aux['nombres'] = item.nombres
        aux['apellidos'] = item.apellidos
        aux['nacimiento'] = unicode(item.fecha_nacimiento)
        aux['direccion'] = unicode(item.pais)+','+unicode(item.ciudad)+','+unicode(item.direccion)
        aux['email'] = item.email
        aux['telefono'] = item.telefono
        aux['acciones'] = '<table  style ="width:100%; border:0px; padding:0px;"><tbody><tr><td style="width:50px; border:0px; padding:0px;"><button name="log" cliente="'+unicode(item.id)+'" class="btn btn-default nav-pill waves-effect waves-block toggled"><i class="material-icons">info</i></button></td><td style="width:50px; border:0px; padding:0px;"><button name="pdf_ficha" cliente="'+unicode(item.id)+'" class="btn btn-default nav-pill waves-effect waves-block toggled"><i class="material-icons">print</i></button></td><td style="width:50px; border:0px; padding:0px;"><button name="editar_cliente"   cliente="'+unicode(item.id)+'" class="btn btn-default nav-pill waves-effect waves-block toggled" ><i class="material-icons">edit</i></button></td></tr></tbody></table>'
        data_table.append(aux)

    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def json_pdf_ficha_ingreso(request):
    if request.method == 'POST':
    #if True:
        content = None
        styles=None
        images=None
        if request.POST.has_key('cliente'):
            cliente = ManagerCliente.obtener_cliente(request.POST.get('cliente'))
            full_name = cliente.nombres+' '+cliente.apellidos
            rut = unicode(cliente.rut)+'-'+unicode(cliente.digito_verificador)
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