# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from cuenta_monetaria.models import Cuenta, TipoTransaccionCuenta, TransaccionCuenta, TipoTransaccionCuentaPrincipal, TransaccionCuentaPrincipal

from cliente.framework import ManagerCliente
from cliente.empresa.framework import ManagerEmpresa

from django.contrib.auth.models import User

class ManagerCuenta():
    """
        Clase para administrar las cuentas de Clientes y empresas
    """
    MODELOS = {
        'CLIENTE' : 'cl',
        'EMPRESA' : 'emp',
    }

    TIPOS_TRANSACCION = {
        'CUENTA_NUEVA':'CUENTA_NUEVA',
        'ABONO':'ABONO',
        'CARGO':'CARGO',
    }

    @staticmethod
    def obtener_cuenta(id):
        """
            Función que obtiene la cuenta monetaria
            Param:
                id: id de la cuenta
            Return:
                Cuenta
                None en caso de no existir la Cuenta
        """
        try:
            return Cuenta.objects.get(id=id)
        except Exception,e:
            return None

    @staticmethod
    def obtener_cuentas(**kwargs):
        """
            Función que obtiene las cuentas monetarias según los filtros correspondientes
            Param:
                ids
                modelo
                modelo_id
                modelo_ids
            Return:
                ResultSet<Cuenta>
        """
        cuentas = Cuenta.objects.all()
        if 'ids' in kwargs:
            cuentas = cuentas.filter(id__in=kwargs['ids'])
        if 'modelo' in kwargs:
            cuentas = cuentas.filter(modelo=kwargs['modelo'])
        if 'modelo_id' in kwargs:
            cuentas = cuentas.filter(modelo_id=kwargs['modelo_id'])
        if 'modelo_ids' in kwargs:
            cuentas = cuentas.filter(modelo_id__in=kwargs['modelo_ids'])
        return cuentas


    @staticmethod
    def crear_cuenta(modelo, modelo_id, user_id):
        """
            Función para crear una nueva cuenta moneraria:
            Params:
                modelo: Modelo según ManagerCuenta.MODELOS
                modelo_id: id del modelo de la cuenta(Empresa o Cliente)
                user_id:La primera transaccion, crear cuenta séra asociada a este usuario.
            Return:
                Cuenta
        """
        cuentas = ManagerCuenta.obtener_cuentas(modelo=modelo, modelo_id=modelo_id)
        if len(cuentas) > 0:
            return cuentas[0]
        if modelo == MODELOS['CLIENTE']:
            if ManagerCliente.obtener_cliente(modelo_id) is None:
                raise Exception('No existe cliente')
        elif modelo == MODELOS['EMPRESA']:
            if ManagerEmpresa.obtener_empresa(modelo_id) is None:
                raise Exception('No existe empresa')
        else:
            raise Exception('Modelo incorrecto')
        cuenta = Cuenta(
                modelo = modelo,
                modelo_id = modelo_id,
                saldo = 0,
                ultima_actualizacion = datetime.now(),
            )
        cuenta.save()
        #TODO: Crear transacción inicial de la cuenta

        return cuenta
    


    @staticmethod
    def obtener_tipotransaccioncuenta(**kwargs):
        """
            Función que obtiene el tipo de transacción cuenta
            Param:
                id: id del tipo de transacción
                nombre: id del tipo de transacción
            Return:
                TipoTransaccionCuenta
                None en caso de no existir
        """
        try:
            if 'id' in kwargs:
                return TipoTransaccionCuenta.objects.get(id=kwargs['id'])
            if 'nombre' in kwargs:
                return TipoTransaccionCuenta.objects.get(nombre=kwargs['nombre'])
            return None
        except Exception,e:
            return None

    @staticmethod
    def obtener_tipostransaccioncuenta(id):
        """
            Función que obtiene los tipos de transacción cuenta
            Param:
                ids:
                nombres: 
            Return:
                ResultSet<TipoTransaccionCuenta>
                None en caso de no existir
        """
        tipostransaccioncuenta = TipoTransaccionCuenta.objects.all()
        if 'ids' in kwargs:
            tipostransaccioncuenta = tipostransaccioncuenta.filter(ids=kwargs['ids'])
        if 'nombre' in kwargs:
            tipostransaccioncuenta = tipostransaccioncuenta.filter(nombre=kwargs['nombre'])
        if 'nombres' in kwargs:
            tipostransaccioncuenta = tipostransaccioncuenta.filter(nombre__in=kwargs['nombres'])
        return tipostransaccioncuenta

    @staticmethod
    def crear_tipostransaccioncuenta(nombre):
        """
            Función para crear un nuevo tipo de transacción.
            Params:
                Nombre
            Return 
                TipoTransaccionCuenta
        """
        tipotransaccioncuenta = ManagerCuenta.obtener_tipotransaccioncuenta(nombre=nombre)
        if tipotransaccioncuenta is not None:
            return tipotransaccioncuenta
        tipotransaccioncuenta = TipoTransaccionCuenta(nombre=nombre)
        tipotransaccioncuenta.save()
        return tipotransaccioncuenta

    @staticmethod
    def inicializar_tipostransaccioncuenta():
        """
            Función para inicializar los tipos de transacción, iniciales del sistema.
            Params:
            Return:
        """
        for key in TIPOS_TRANSACCION:
            if ManagerCuenta.obtener_tipotransaccioncuenta(nombre=TIPOS_TRANSACCION[key]) is None:
                ManagerCuenta.crear_cuenta(nombre=TIPOS_TRANSACCION[key])


    @staticmethod
    def crear_transaccioncuenta(cuenta_id, user_id, tipotransaccioncuenta_nombre, cargo, abono,
                             reservaalojamiento_id=None, ocupacionalojamiento_id=None,  
                             descripcion = '',
                             ):
        """
            Función para crear una nueva transacción de cuenta.

        """
    cuenta = ManagerCuenta.obtener_cuenta(cuenta_id)
    aux = 
    user = 

    transaccion 
    TransaccionCuenta


    
    reservaalojamiento = models.ForeignKey(ReservaAlojamiento, models.DO_NOTHING, null=True)
    ocupacionalojamiento = models.ForeignKey(OcupacionAlojamiento, models.DO_NOTHING, null=True)
    tipotransaccioncuenta = models.ForeignKey(TipoTransaccionCuenta, models.DO_NOTHING)
    descripcion = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cargo = models.FloatField(default=0)
    abono = models.FloatField(default=0)
    saldo = models.FloatField(default=0)