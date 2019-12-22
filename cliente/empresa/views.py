# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .framework import ManagerEmpresa
from apps import EmpresaConfig




@login_required
def view_lista_empresa(request):
    context = {}
    return render(request, EmpresaConfig.name+'/lista_empresa.html', context)


@login_required
def json_lista_empresa(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Rut', 'data':'rut'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Teléfono', 'data':'telefono'});
    columnas.append({'title':'Dirección', 'data':'direccion'});
    columnas.append({'title':'Email', 'data':'email'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});
    columnas.append({'title':'Acciones', 'data':'acciones'});

    empresas = ManagerEmpresa.obtener_empresas()
    data_table = []
    for item in empresas:
        aux = {}
        aux['id'] = item.id
        aux['rut'] = unicode(item.rut)+'-'+unicode(item.digito_verificador)
        aux['nombre'] = item.nombre
        aux['telefono'] = item.telefono
        aux['direccion'] = unicode(item.ciudad)+','+unicode(item.direccion)
        aux['email'] = item.email
        aux['descripcion'] = item.descripcion
        aux['acciones'] = '<table style="width:100%; border:0px; padding:0px;"><tbody><tr><td style="width:50px; border:0px; padding:0px;"> <button name="log" empresa="'+unicode(item.id)+'" class="btn bg-indigo nav-pill waves-effect waves-block toggled"><i class="material-icons">info</i></button> </td><td style="width:50px; border:0px; padding:0px;"> <button name="ver_cliente_asociado" empresa="'+unicode(item.id)+'" empresa_nombre="'+item.nombre+'" class="btn bg-indigo nav-pill waves-effect waves-block toggled"><i class="material-icons">people_outline</i></button> </td></tr></tbody></table>'
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)

@login_required
def json_lista_clientes_asociados_empresa(request):
    if not 'empresa_id' in request.POST:
        return JsonResponse({
                'data':[],
                'columnas':[],
            })
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Rut', 'data':'rut'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Teléfono', 'data':'telefono'});
    columnas.append({'title':'Email', 'data':'email'});

    empresa_id = request.POST.get('empresa_id')
    asociacion_clientes = ManagerEmpresa.obtener_asociacionclienteempresa(empresa_id=empresa_id)
    asociacion_clientes = asociacion_clientes.select_related('cliente')
    data_table = []
    for item in asociacion_clientes:
        aux = {}
        aux['id'] = item.cliente.id
        aux['rut'] = unicode(item.cliente.rut)+'-'+unicode(item.cliente.digito_verificador)
        aux['nombre'] = item.cliente.nombres+' '+item.cliente.apellidos
        aux['telefono'] = item.cliente.telefono
        aux['email'] = item.cliente.email
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)