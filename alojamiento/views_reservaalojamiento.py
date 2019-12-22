# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db import transaction

from apps import AlojamientoConfig

from framework import ManagerAlojamiento
from framework_2 import ManagerOcupacionAlojamiento
from alojamiento.tarifa.framework import ManagerTarifa, ManagerTemporada

@login_required
def view_lista_reservaalojamiento(request):
    context = {}
    return render(request, AlojamientoConfig.name+'/lista_reservaalojamiento.html', context)

@login_required
def json_lista_comentario(request):
    comentarios = ManagerOcupacionAlojamiento.obtener_comentarios()
    data = []
    for comentario in comentarios:
        data.append({
            'id':comentario.id,
            'texto':comentario.texto
            })
    retorno = {
        'state':'success',
        'comentarios':data,
    }
    return JsonResponse(retorno, safe=False)

def json_data_ocupacionalojamiento(request):
    retorno = {
        'state':'success',
        'info_alojamientos':[],
        'grupos':[],
        'items':[{
            "id": -1,
            "content": "",
            "start": unicode(datetime.today().year)+"-"+unicode(datetime.today().month)+"-"+unicode(datetime.today().day)+" 00:00:00",
            "end": unicode(datetime.today().year)+"-"+unicode(datetime.today().month)+"-"+unicode(datetime.today().day)+" 23:59:00",
            "type": "background",
        }],
    }
    grupo_temporada = {
        'id': -9999999,
        'content': 'TEMPORADAS',
        'nestedGroups': [],
        'showNested': True,
    }
    temporadas = ManagerTemporada.obtener_temporadas()
    for temporada in temporadas:
        grupo_temporada['nestedGroups'].append(temporada.id+100000000)
        retorno['grupos'].append({
            'id': temporada.id+100000000,
            'content': temporada.nombre,
        })
    temporadasfecha = ManagerTemporada.obtener_temporadasfecha().order_by('fecha')
    aux_fecha = None
    aux = None
    for temporadafecha in temporadasfecha:
        if aux is not None:
            if aux['group'] == temporadafecha.temporada_id+100000000 and temporadafecha.fecha == aux_fecha + timedelta(days=1):
                aux_fecha = aux_fecha + timedelta(days=1)
            else:
                aux["end"] = unicode(aux_fecha.year)+"-"+unicode(aux_fecha.month)+"-"+unicode(aux_fecha.day)+" 23:59:59"
                retorno['items'].append(aux)
                aux = None
        if aux is None:
            aux = {
                "id": temporadafecha.id+100000000,
                "content": "",
                "start": unicode(temporadafecha.fecha.year)+"-"+unicode(temporadafecha.fecha.month)+"-"+unicode(temporadafecha.fecha.day)+" 0:00:00",
                "end": None,
                "type": "background",
                "group": temporadafecha.temporada_id+100000000,
                "className":"temporada",
            }
            aux_fecha = temporadafecha.fecha
    if aux is not None:
        aux["end"] = unicode(aux_fecha.year)+"-"+unicode(aux_fecha.month)+"-"+unicode(aux_fecha.day)+" 23:59:59"
        retorno['items'].append(aux)
        aux=None
    retorno['grupos'].append(grupo_temporada)
    tiposalojamiento = ManagerAlojamiento.obtener_tiposalojamiento()
    for tipoalojamiento in tiposalojamiento:
        info = {
            'tipoalojamiento':{
                'id': tipoalojamiento.id,
                'nombre': tipoalojamiento.nombre,
            },
            'alojamientos':[]
        }
        dic = {
            'id': tipoalojamiento.id+100000,
            'content': tipoalojamiento.nombre,
            'nestedGroups': [],
            'showNested': True,
        }
        alojamientos = ManagerAlojamiento.obtener_alojamientos(
          tipoalojamiento_id=tipoalojamiento.id,
        )
        for alojamiento in alojamientos:
            info['alojamientos'].append({
                'id': alojamiento.id,
                'codigo': alojamiento.codigo,
            })
            retorno['grupos'].append({
                'id': alojamiento.id,
                'content': alojamiento.codigo,
            })
            dic['nestedGroups'].append(alojamiento.id)
        if len(dic['nestedGroups']) > 0:
            retorno['grupos'].append(dic)
            retorno['info_alojamientos'].append(info)
    ocupacionesalojamientos = ManagerOcupacionAlojamiento.obtener_ocupacionesalojamiento()
    alojamientos = ManagerAlojamiento.obtener_alojamientos()
    for alojamiento in alojamientos:
        ocupacionesalojamiento = ocupacionesalojamientos.filter(alojamiento_id=alojamiento.id).select_related('reservaalojamiento').order_by('fecha','reservaalojamiento')
        aux_fecha = None
        aux = None
        for ocupacionalojamiento in ocupacionesalojamiento:
            if aux is not None:
                if aux['group'] == ocupacionalojamiento.alojamiento_id and aux['reservaalojamiento'] == ocupacionalojamiento.reservaalojamiento_id and ocupacionalojamiento.fecha == aux_fecha + timedelta(days=1):
                    aux_fecha = aux_fecha + timedelta(days=1)
                else:
                    aux["end"] = unicode(aux_fecha.year)+"-"+unicode(aux_fecha.month)+"-"+unicode(aux_fecha.day)+" 23:59:59"
                    retorno['items'].append(aux)
                    aux = None
            if aux is None:
                aux = {
                    "id": ocupacionalojamiento.id,
                    "reservaalojamiento":ocupacionalojamiento.reservaalojamiento_id,
                    "content": '<div name="item_ocupacion" reserva_id="'+unicode(ocupacionalojamiento.reservaalojamiento_id)+'" >R_'+unicode(ocupacionalojamiento.reservaalojamiento_id)+'</div>',
                    "start": unicode(ocupacionalojamiento.fecha.year)+"-"+unicode(ocupacionalojamiento.fecha.month)+"-"+unicode(ocupacionalojamiento.fecha.day)+" 0:00:00",
                    "end": None,
                    "type": "range",
                    # "type": "background",
                    "group": ocupacionalojamiento.alojamiento_id,
                    "className":"estado_"+ocupacionalojamiento.reservaalojamiento.estado
                }
                aux_fecha = ocupacionalojamiento.fecha
        if aux is not None:
            aux["end"] = unicode(aux_fecha.year)+"-"+unicode(aux_fecha.month)+"-"+unicode(aux_fecha.day)+" 23:59:59"
            retorno['items'].append(aux)
            aux=None
    return JsonResponse(retorno, safe=False)



def json_comprobarocupacion(request):
    context = {}
    if request.method == 'POST':
        post_dic = json.loads(request.POST.get('datos'))
        fecha_inicial = datetime.date(datetime.strptime(post_dic['fecha_inicial'], "%Y-%m-%d"))
        fecha_final = datetime.date(datetime.strptime(post_dic['fecha_final'], "%Y-%m-%d"))
        errores = ''
        print post_dic
        flag, errores =  ManagerOcupacionAlojamiento.comprobar_ocupacionalojamiento(
            alojamiento_id=int(post_dic['alojamiento_id']),
            numero_personas=int(post_dic['numero_personas']),
            fecha_inicio=fecha_inicial,
            fecha_final=fecha_final,
            cautiva=post_dic['cautiva'],
            canalventa_id=int(post_dic['canal_venta']),
            tarifa_id=int(post_dic['tarifa']),
        )
        if flag:
            alojamiento = ManagerAlojamiento.obtener_alojamiento(int(post_dic['alojamiento_id']))
            temporada = ManagerTemporada.obtener_temporadafecha(fecha=fecha_inicial).temporada
            flag, errores = ManagerTarifa.comprobar_tarifa_valida(
                tarifa_id=int(post_dic['tarifa']),
                cliente_id=int(post_dic['cliente']),
                temporada_id=temporada.id,
                canalventa_id=int(post_dic['canal_venta']),
                tipoalojamiento_id=alojamiento.tipoalojamiento_id,
            )
        if flag:
            return JsonResponse({
                'state':'success',
            }, safe=False)
        return JsonResponse({
                'state':'error',
                'messages':[{
                    'state':'error',
                    'text':errores,
                }]
            }, safe=False)
    retorno = {
        'state':'success',
    }
    # tiposalojamiento = ManagerAlojamiento.obtener_tiposalojamiento()
    return JsonResponse(retorno, safe=False)

@transaction.atomic
def json_crear_reserva (request):
    if request.method == 'POST':
        post_dic = json.loads(request.POST.get('datos'))
        print post_dic
        for alojamiento_reserva in post_dic['reservas']:
            fecha_inicial = datetime.date(datetime.strptime(alojamiento_reserva['fecha_inicial'], "%Y-%m-%d"))
            fecha_final = datetime.date(datetime.strptime(alojamiento_reserva['fecha_final'], "%Y-%m-%d"))
            flag, errores =  ManagerOcupacionAlojamiento.comprobar_ocupacionalojamiento(
                alojamiento_id=int(alojamiento_reserva['alojamiento_id']),
                numero_personas=int(alojamiento_reserva['numero_personas']),
                fecha_inicio=fecha_inicial,
                fecha_final=fecha_final,
                cautiva=alojamiento_reserva['cautiva'],
                canalventa_id=int(alojamiento_reserva['canal_venta']),
                tarifa_id=int(alojamiento_reserva['tarifa']),
            )
            if flag:
                alojamiento = ManagerAlojamiento.obtener_alojamiento(int(alojamiento_reserva['alojamiento_id']))
                temporada = ManagerTemporada.obtener_temporadafecha(fecha=fecha_inicial).temporada
                flag, errores = ManagerTarifa.comprobar_tarifa_valida(
                    tarifa_id=int(alojamiento_reserva['tarifa']),
                    cliente_id=int(post_dic['cliente']),
                    temporada_id=temporada.id,
                    canalventa_id=int(alojamiento_reserva['canal_venta']),
                    tipoalojamiento_id=alojamiento.tipoalojamiento_id,
                )
            if not flag:
                return JsonResponse({
                    'state':'error',
                    'messages':[{
                        'state':'error',
                        'text':'Petición corrupta.(JCR1)',
                    }]
                }, safe=False)
        try:
            with transaction.atomic():
                reservaalojamiento = ManagerOcupacionAlojamiento.crear_reservaalojamiento(estado=ManagerOcupacionAlojamiento.ESTADOS_RESERVA['CONFIRMANDO_PAGO'], fecha_reservacion=datetime.today(), cliente_id=post_dic['cliente'], empresa_id=None, user_id=request.user.id)
                comentarios_reserva = []
                for alojamiento_reserva in post_dic['reservas']:
                    if alojamiento_reserva['comentarios']:
                        alojamiento = ManagerAlojamiento.obtener_alojamiento(int(alojamiento_reserva['alojamiento_id']))
                        comentarios_reserva.append({
                            'codigo':alojamiento.codigo,
                            'comentario':alojamiento_reserva['comentarios'],
                        })
                    fecha_inicial = datetime.date(datetime.strptime(alojamiento_reserva['fecha_inicial'], "%Y-%m-%d"))
                    fecha_final = datetime.date(datetime.strptime(alojamiento_reserva['fecha_final'], "%Y-%m-%d"))
                    aux_fecha = fecha_inicial
                    tarifa = ManagerTarifa.obtener_tarifa(alojamiento_reserva['tarifa'])
                    while aux_fecha <= fecha_final:
                        valores = tarifa.valores
                        dia_bdd = (aux_fecha.isoweekday() % 7) + 1
                        aux_valor = valores[unicode(dia_bdd)][alojamiento_reserva['numero_personas']]
                        nueva_opcupacion = ManagerOcupacionAlojamiento.crear_ocupacionalojamiento(
                            alojamiento_id=int(alojamiento_reserva['alojamiento_id']), 
                            reservaalojamiento_id=reservaalojamiento.id,
                            huespedes=int(alojamiento_reserva['numero_personas']),
                            fecha=aux_fecha,
                            canalventa_id=int(alojamiento_reserva['canal_venta']), 
                            tarifa_id=int(alojamiento_reserva['tarifa']),
                            valor=aux_valor,
                            cautiva=alojamiento_reserva['cautiva'],
                            user_id=request.user.id
                        )
                        aux_fecha = aux_fecha + timedelta(days=1)
                aux_dic = {}
                i=0
                while i < len(comentarios_reserva):
                    aux_dic[unicode(i)] =comentarios_reserva[i]
                    i+=1
                ManagerOcupacionAlojamiento.editar_reservaalojamiento(reservaalojamiento_id=reservaalojamiento.id ,comentario=aux_dic, user_id=request.user.id)
                return JsonResponse({
                    'state':'success',
                    'reserva':reservaalojamiento.id,
                }, safe=False)
        except Exception,e:
            print e
            return JsonResponse({
            'state':'error',
            'messages':[{
                    'state':'error',
                    'text':'Petición corrupta.(JCR2)',
                }]
            }, safe=False)
    return JsonResponse({
            'state':'error',
            'messages':[{
                        'state':'error',
                        'text':'Petición corrupta.',
                    }]
        }, safe=False)
