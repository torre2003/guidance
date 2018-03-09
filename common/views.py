# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse



from apps import CommonConfig
from cliente.empresa.framework import ManagerEmpresa as me
from alojamiento.tarifa.framework import ManagerTemporada as mt
from alojamiento.tarifa.framework import ManagerTarifa as mta
from alojamiento.framework import ManagerAlojamiento as ma
from alojamiento.framework import ManagerCanalVenta as mcv
from alojamiento.framework_2 import ManagerOcupacionAlojamiento as moa


@login_required
def view_datatable(request):
    context = {}
    context["id"] = request.POST.get('id', '')
    context["clases"] = request.POST.get('clases', '')
    context['titulo'] = request.POST.get('titulo', '')
    return render(request, CommonConfig.name+'/container_datatable.html', context)


@login_required
def view_test(request):
    context = {}
    return render(request, CommonConfig.name+'/test.html', context)


@login_required
def json_test_01(request):
    print '*'*10,'   Test-01    ','*'*10
    # ma.crear_tipoalojamiento (nombre=u'cabañas tipo 3.1', descripcion=u'Cabañas del rey de las vacas', capacidad=1, habilitado=True, user_id=1)
    ma.editar_tipoalojamiento (tipoalojamiento_id=3, nombre=u'cabañas tipo 3.3', descripcion=u'Cabañas del rey de las vacas..', capacidad=3, habilitado=True, user_id=1)
    print '*'*10,'   Test-01    ','*'*10
    return JsonResponse({})


@login_required
def json_test_02(request):
    print '*'*10,'   Test-02    ','*'*10
    ma.crear_alojamiento(nombre='Cabaña Verde 7', codigo='CV7', tipoalojamiento_id=2, user_id=request.user.id)
    print '*'*10,'   Test-02    ','*'*10
    return JsonResponse({})

@login_required
def json_test_03(request):
    print '*'*10,'   Test-03    ','*'*10
    ma.editar_alojamiento(alojamiento_id=1,nombre='Cabaña Naranja 1', codigo='CN1', tipoalojamiento_id=1, user_id=request.user.id)
    print '*'*10,'   Test-03    ','*'*10
    return JsonResponse({})


@login_required
def json_test_04(request):
    print '*'*10,'   Test-04    ','*'*10
    # mcv.crear_canalventa (nombre="Trivago", descripcion="Sitio, Poleras blancas", habilitado=FalseTrue, user_id=request.user.id)
    mcv.editar_canalventa (canalventa_id=1, nombre="El mostrador 1.1", descripcion="Sitio, le mostrador XY ", habilitado=True, user_id=request.user.id)
    mcv.editar_canalventa (canalventa_id=2, nombre="Trivago_", descripcion="Sitio, Poleras blancas_", habilitado=True, user_id=request.user.id)
    print '*'*10,'   Test-04    ','*'*10
    return JsonResponse({})


@login_required
def json_test_05(request):
    print '*'*10,'   Test-05    ','*'*10
    print mt.editar_temporada(1,nombre='Temporada_Baja', descripcion='Temporada general del año. 29 Mar -- 20 Diciembre', user_id=request.user.id)
    print '*'*10,'   Test-05    ','*'*10
    return JsonResponse({})


@login_required
def json_test_06(request):
    print '*'*10,'   Test-06    ','*'*10

    mta.crear_tarifa(
        nombre='Tarifa promocional verano 2017', 
        descripcion='Tarifa para captar clientes', 
        habilitado=False,
        restricciones = {
            # 'temporadas':[1],
            'dias': [1,4,5,6],
            'tipos_alojamiento':[1,2],
            # 'empresas':[1,2],
        },
        valores={
            1:10000.5,
            2:10000,
            3:20000,
            4:20000,
            5:30000,
        },
        user_id=request.user.id
    )

    print '*'*10,'   Test-06    ','*'*10
    return JsonResponse({})




@login_required
def json_test_07(request):
    print '*'*10,'   Test-07    ','*'*10
    """
    mta.editar_tarifa(
        tarifa_id=1,
        nombre='C. Verde - Baja Eco y Zurla.', 
        descripcion='Tarifa de las cabañas verdes en temporada baja para empresas Eco y Zurla.', 
        habilitado=False,
        restricciones = {
            'temporadas':[1],
            'dias': [1,2,3,4,5,6],
            'tipos_alojamiento':[2],
            'empresas':[1,2],
        },
        valores={
            1:12000.5,
            2:15000,
            3:20000,
            4:20000,
            5:60500,
        },
        user_id=request.user.id
    )
    """
    mta.crear_tarifa(
        nombre='Weekend',
        descripcion='Tarifa para fines de semana.',
        habilitado=True,
        restricciones={
            'dias': [1,7],
        },
        valores={
            1:35000,
            2:35000,
            3:45000,
            4:45000,
            5:55000,
            6:55000,
        },
        user_id=request.user.id
    )
    print '*'*10,'   Test-07    ','*'*10
    return JsonResponse({})


@login_required
def json_test_08(request):
    print '*'*10,'   Test-08    ','*'*10
    if False:
        moa.crear_reservaalojamiento(
            estado=moa.ESTADOS_RESERVA['CONFIRMANDO_PAGO'],
            fecha_reservacion=datetime.today()+timedelta(days=1),
            cliente_id=1,
            empresa_id=1,
            # canalventa_id=1,
            user_id=request.user.id
        )
    if True:
        moa.editar_reservaalojamiento(
            reservaalojamiento_id = 6,
            estado=moa.ESTADOS_RESERVA['CONFIRMADA'],
            fecha_reservacion=datetime.today(),
            cliente_id=2,
            empresa_id=2,
            # canalventa_id=1,
            user_id=request.user.id
        )
    print '*'*10,'   Test-08    ','*'*10
    return JsonResponse({})


@login_required
def json_test_09(request):
    print '*'*10,'   Test-09    ','*'*10
    if True:
        moa.crear_ocupacionalojamiento(
            alojamiento_id=1,
            reservaalojamiento_id=1,
            huespedes=2,
            fecha=datetime.today(),
            canalventa_id=1,
            tarifa_id=1,
            valor=15000,
            cautiva=True,
            user_id=request.user.id,
        )
    if True:
        moa.editar_ocupacionalojamiento(
            ocupacionalojamiento_id=1,
            alojamiento_id=1,
            reservaalojamiento_id=2,
            huespedes=3,
            fecha=datetime.today()+timedelta(days=1),
            canalventa_id=2,
            tarifa_id=2,
            valor=25000,
            cautiva=False,
            user_id=request.user.id,
        )
    print '*'*10,'   Test-09    ','*'*10
    return JsonResponse({})