# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from .framework import ManagerTemporada, ManagerTarifa
from alojamiento.framework import ManagerAlojamiento, ManagerCanalVenta
from cliente.empresa.framework import ManagerEmpresa
from apps import TarifaConfig

from common import utils as utils_common

# Create your views here.
@login_required
def view_lista_temporada(request):
    context = {}
    return render(request, TarifaConfig.name+'/lista_temporada.html', context)


@login_required
def json_lista_temporada(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});

    temporadas = ManagerTemporada.obtener_temporadas()
    data_table = []
    for item in temporadas:
        aux = {}
        aux['id'] = item.id
        aux['nombre'] = item.nombre
        aux['descripcion'] = item.descripcion
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)

@login_required
def json_lista_temporadafecha(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'Fecha', 'data':'fecha'});

    temporadas = ManagerTemporada.obtener_temporadas().order_by('id')
    temporadas_ids = []
    for item in temporadas:
        aux = {}
        aux['title'] = item.nombre
        aux['data'] = unicode(item.id)
        aux['className'] = "text-center"
        temporadas_ids.append(item.id)
        columnas.append(aux)
    print temporadas_ids
    
    temporadasfecha = ManagerTemporada.obtener_temporadasfecha().order_by('fecha')
    data_table = []
    for item in temporadasfecha:
        aux = {}
        aux['fecha'] = unicode(item.fecha)
        for temporada_id in temporadas_ids:
            aux[unicode(temporada_id)] = '   '
        aux[unicode(item.temporada_id)] = '<i class="material-icons">center_focus_weak</i>'

        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def view_lista_tarifa(request):
    context = {}
    return render(request, TarifaConfig.name+'/lista_tarifa.html', context)


@login_required
def json_lista_tarifa(request):
    respuesta = {}
    columnas = []
    columnas.append({'title':'ID', 'data':'id'});
    columnas.append({'title':'Nombre', 'data':'nombre'});
    columnas.append({'title':'Descripción', 'data':'descripcion'});
    columnas.append({'title':'Valores x persona', 'data':'valores'});
    columnas.append({'title':'Restricciones', 'data':'restricciones'});
    columnas.append({'title':'Habilitado', 'data':'habilitado'});

    tarifas = ManagerTarifa.obtener_tarifas()
    data_table = []
    for item in tarifas:
        aux = {}
        aux['id'] = item.id
        aux['nombre'] = item.nombre
        aux['descripcion'] = item.descripcion
        aux['habilitado'] = '<i class="material-icons text-green">check</i>'
        if not item.habilitado:
            aux['habilitado'] = '<i class="material-icons text-red">clear</i>'
        aux['valores']= ''
        print '**'*15
        print item.valores.keys()
        print item.valores['1']
        dias = [2, 3, 4, 5, 6, 7, 1]
        nombre_dias = ['---','Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        if item.id == item.id:
            thead = ''
            tbody = ''
            i=0
            while i <= 7:
                j=0
                while j <= 10:
                    # if i != 0:
                    #     tbody += '<tr>'
                    if i== 0 and j==0:
                        thead += '<th></th>'
                    elif i == 0:
                        thead += '<th>'+unicode(j)+'</th>'
                    elif j == 0:
                        tbody += '<tr><th>'+nombre_dias[i]+'</th>'
                    else:
                        if unicode(j) in item.valores[unicode(i)]:
                            tbody += '<td>'+unicode(item.valores[unicode( dias[i-1] )][unicode(j)])+'</td>'
                        else:
                            tbody += '<td>---</td>'
                    j+=1
                tbody += '</tr>'
                i+=1
            print '+'*13
            print tbody
            print '+'*13
            print item.valores
            aux['valores'] += '<table>'
            aux['valores'] += '<thead>'
            aux['valores'] += thead
            aux['valores'] += '</thead>'
            aux['valores'] += '<tbody>'
            aux['valores'] += tbody
            aux['valores'] += '</tbody>'
            aux['valores'] += '</table>'

        

        
        # for k in k_valores:
            
            # aux['valores'] += '<strong>'+unicode(k)+':</strong> $'+ utils_common.formato_numero(item.valores[k])+'<br />'

        aux['restricciones'] = ''
        aux['restricciones'] += '<strong>Temporadas:</strong>'
        if 'temporadas' in item.restricciones:
            for temporada in ManagerTemporada.obtener_temporadas(ids=item.restricciones['temporadas']):
                aux['restricciones'] += temporada.nombre+' | '
        else:
            aux['restricciones'] += '----'
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Tipo de alojamiento:</strong>'
        if 'tipos_alojamiento' in item.restricciones:
            for tipoalojamiento in ManagerAlojamiento.obtener_tiposalojamiento(ids=item.restricciones['tipos_alojamiento']):
                aux['restricciones'] += tipoalojamiento.nombre+' | '
        else:
            aux['restricciones'] += '----'
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Empresas:</strong>'
        if 'empresas' in item.restricciones:
            for empresas in ManagerEmpresa.obtener_empresas(ids=item.restricciones['empresas']):
                aux['restricciones'] += empresas.nombre+' | '
        else:
            aux['restricciones'] += '----'
        aux['restricciones'] += '<br />'
        aux['restricciones'] += '<strong>Canales de venta:</strong>'
        if 'canales_venta' in item.restricciones:
            for canal_venta in ManagerCanalVenta.obtener_canalesventa(ids=item.restricciones['canales_venta']):
                aux['restricciones'] += canal_venta.nombre+' | '
        else:
            aux['restricciones'] += '----'
        aux['restricciones'] += '<br />'
        # if 
        # aux['restricciones'] = unicode(item.restricciones)
        data_table.append(aux)
    respuesta['data']=data_table
    respuesta['columnas'] = columnas
    return JsonResponse(respuesta)


@login_required
def json_obtener_tarifas(request):
    print '*'*15
    tarifas = ManagerTarifa.obtener_tarifas()
    aux_tarifas = []
    for tarifa in tarifas:
        aux = tarifa.__dict__
        aux['_state']=''
        aux['valores']=tarifa.valores
        aux['restricciones']=tarifa.restricciones
        i=0
        while i < len(aux['restricciones']['canales_venta']):
            canal_venta = ManagerCanalVenta.obtener_canalventa(aux['restricciones']['canales_venta'][i])
            aux['restricciones']['canales_venta'][i] = {
                'id':canal_venta.id,
                'nombre':canal_venta.nombre,
            }
            i+=1
        i=0
        while i < len(aux['restricciones']['empresas']):
            empresa = ManagerEmpresa.obtener_empresa(aux['restricciones']['empresas'][i])
            aux['restricciones']['empresas'][i] = {
                'id':empresa.id,
                'nombre':empresa.nombre,
            }
            i+=1
        i=0
        while i < len(aux['restricciones']['temporadas']):
            temporada = ManagerTemporada.obtener_temporada(aux['restricciones']['temporadas'][i])
            aux['restricciones']['temporadas'][i] = {
                'id':temporada.id,
                'nombre':temporada.nombre,
            }
            i+=1
        i=0
        while i < len(aux['restricciones']['tipos_alojamiento']):
            tipo_alojamiento = ManagerAlojamiento.obtener_tipoalojamiento(aux['restricciones']['tipos_alojamiento'][i])
            aux['restricciones']['tipos_alojamiento'][i] = {
                'id':tipo_alojamiento.id,
                'nombre':tipo_alojamiento.nombre,
            }
            i+=1
        aux_tarifas.append(aux)
    respuesta = {
        'state':'success',
        'tarifas':aux_tarifas,
    }
    return JsonResponse(respuesta, safe=False)