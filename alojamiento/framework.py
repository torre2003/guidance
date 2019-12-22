# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from models import CanalVenta, TipoAlojamiento, Alojamiento, ReservaAlojamiento, OcupacionAlojamiento
from models import LogAlojamiento as Log
from django.contrib.auth.models import User


class ManagerAlojamiento():
    """
        Clase para administrar Alojamientos y Tipo Alojamiento
    """

    @staticmethod
    def obtener_tipoalojamiento(id):
        """
            Función que obtiene el TipoAlojamiento
            Param:
                id: id de la TipoAlojamiento
            Return:
                TipoAlojamiento
                None en caso de no existir el TipoAlojamiento
        """
        try:
            return TipoAlojamiento.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_tiposalojamiento(**kwargs):
        """
            Función para recuperar los TipoAlojamiento
            Param:
                ids
                nombre
            Return:
                ResultSet<TipoAlojamiento>
        """
        tiposalojamiento = TipoAlojamiento.objects.all()
        if 'ids' in kwargs:
            tiposalojamiento = tiposalojamiento.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            tiposalojamiento = tiposalojamiento.filter(nombre=kwargs['nombre'])
        if 'habilitado' in kwargs:
            tiposalojamiento = tiposalojamiento.filter(habilitado=kwargs['habilitado'])
        return tiposalojamiento

    @staticmethod
    def crear_tipoalojamiento (nombre, descripcion, capacidad, habilitado, user_id=None):
        """
            Función que ingresa un nuevo tipo de alojamiento
            Param:
                nombre,
                descripcion,
                capacidad,
                habilitado,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                TipoAlojamiento
                None en caso de existir el tipoalojamiento en la base de datos
        """
        if len(ManagerAlojamiento.obtener_tiposalojamiento(nombre=nombre)) > 0:
            return None
        aux_tipoalojamiento = TipoAlojamiento(
            nombre=nombre,
            descripcion=descripcion,
            capacidad=capacidad,
            habilitado=habilitado,
        )
        aux_tipoalojamiento.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_tipoalojamiento),
                modelo_id=aux_tipoalojamiento.id, 
                info={'accion':'creación'}
            )
        return aux_tipoalojamiento


    @staticmethod
    def editar_tipoalojamiento (tipoalojamiento_id, nombre=None, descripcion=None, capacidad=None, habilitado=None, user_id=None):
        """
            Función modificar un tipo de alojamiento ya ingresado en la base de datos
            Param:
                tipoalojamiento_id
                nombre,
                descripcion,
                capacidad,
                habilitado,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                TipoAlojamiento
                None en caso de NO existir el tipo de alojamiento en la base de datos
        """
        tipoalojamiento = ManagerAlojamiento.obtener_tipoalojamiento(tipoalojamiento_id)
        if tipoalojamiento is None:
            return None
        info = {}
        if nombre:
            if tipoalojamiento.nombre != nombre:
                info['nombre'] = tipoalojamiento.nombre+' -> '+nombre
                tipoalojamiento.nombre = nombre
        if descripcion:
            if tipoalojamiento.descripcion != descripcion:
                info['descripcion'] = tipoalojamiento.descripcion+' -> '+descripcion
                tipoalojamiento.descripcion = descripcion
        if capacidad:
            if tipoalojamiento.capacidad != capacidad:
                info['capacidad'] = unicode(tipoalojamiento.capacidad)+' -> '+unicode(capacidad)
                tipoalojamiento.capacidad = capacidad
        if habilitado:
            if tipoalojamiento.habilitado != habilitado:
                info['habilitado'] = unicode(tipoalojamiento.habilitado)+' -> '+unicode(habilitado)
                tipoalojamiento.habilitado = habilitado
        tipoalojamiento.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(tipoalojamiento),
                modelo_id=tipoalojamiento.id, 
                info=info
            )
        return tipoalojamiento


    @staticmethod
    def obtener_alojamiento(id):
        """
            Función que obtiene el Alojamiento
            Param:
                id: id de la Alojamiento
            Return:
                Alojamiento
                None en caso de no existir el Alojamiento
        """
        try:
            return Alojamiento.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_alojamientos(**kwargs):
        """
            Función para recuperar los Alojamiento
            Param:
                ids
                nombre
                codigo
                tipoalojamiento_id
                tipoalojamiento_ids
            Return:
                ResultSet<TipoAlojamiento>
        """
        alojamientos = Alojamiento.objects.all()
        if 'ids' in kwargs:
            alojamientos = alojamientos.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            alojamientos = alojamientos.filter(nombre=kwargs['nombre'])
        if 'codigo' in kwargs:
            alojamientos = alojamientos.filter(codigo=kwargs['codigo'])
        if 'tipoalojamiento_id' in kwargs:
            alojamientos = alojamientos.filter(tipoalojamiento_id=kwargs['tipoalojamiento_id'])
        if 'tipoalojamiento_ids' in kwargs:
            alojamientos = alojamientos.filter(tipoalojamiento_id__in=kwargs['tipoalojamiento_ids'])
        return alojamientos

    @staticmethod
    def crear_alojamiento (nombre, codigo, tipoalojamiento_id, user_id=None):
        """
            Función que ingresa un nuevo alojamiento
            Param:
                nombre,
                codigo,
                tipoalojamiento_id,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                Alojamiento
                None en caso de existir el alojamiento en la base de datos
        """
        if len(ManagerAlojamiento.obtener_alojamientos(codigo=codigo)) > 0 :
            return None
        if ManagerAlojamiento.obtener_tipoalojamiento(tipoalojamiento_id) is None:
            raise Exception ('No existe el tipo de alojamiento')
        aux_alojamiento = Alojamiento(
            nombre=nombre,
            codigo=codigo,
            tipoalojamiento_id=tipoalojamiento_id,
        )
        aux_alojamiento.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_alojamiento),
                modelo_id=aux_alojamiento.id,
                info={'accion':'creación'}
            )
        return aux_alojamiento

    @staticmethod
    def editar_alojamiento(alojamiento_id, nombre=None, codigo=None, tipoalojamiento_id=None, user_id=None):
        """
            Función modificar un alojamiento ya ingresado en la base de datos
            Param:
                alojamiento_id
                nombre,
                codigo,
                tipoalojamiento_id,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                Alojamiento
                None en caso de NO existir el alojamiento en la base de datos
        """
        alojamiento = ManagerAlojamiento.obtener_alojamiento(alojamiento_id)
        if alojamiento is None:
            return None
        info = {}
        if nombre:
            if alojamiento.nombre != nombre:
                info['nombre'] = alojamiento.nombre+' -> '+nombre
                alojamiento.nombre = nombre
        if codigo:
            if alojamiento.codigo != codigo:
                info['codigo'] = alojamiento.codigo+' -> '+codigo
                alojamiento.codigo = codigo
        if tipoalojamiento_id:
            tipoalojamiento = ManagerAlojamiento.obtener_tipoalojamiento(tipoalojamiento_id)
            if tipoalojamiento is None:
                raise Exception ('No existe el tipo de alojamiento')
            if alojamiento.tipoalojamiento_id != tipoalojamiento_id:
                info['tipoalojamiento_id'] = unicode(alojamiento.tipoalojamiento_id)+' -> '+unicode(tipoalojamiento_id)
                alojamiento.tipoalojamiento_id = tipoalojamiento_id
        alojamiento.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(alojamiento),
                modelo_id=alojamiento.id, 
                info=info
            )
        return alojamiento


class ManagerCanalVenta():
    """
        Clase para administrar los Canales de venta
    """
    @staticmethod
    def obtener_canalventa(id):
        """
            Función que obtiene el CanalVenta
            Param:
                id: id de la CanalVenta
            Return:
                CanalVenta
                None en caso de no existir el CanalVenta
        """
        try:
            return CanalVenta.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_canalesventa(**kwargs):
        """
            Función para recuperar los CanalVenta
            Param:
                ids
                nombre
            Return:
                ResultSet<TipoAlojamiento>
        """
        canalesventa = CanalVenta.objects.all()
        if 'ids' in kwargs:
            canalesventa = canalesventa.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            canalesventa = canalesventa.filter(nombre=kwargs['nombre'])
        if 'habilitado' in kwargs:
            canalesventa = canalesventa.filter(habilitado=kwargs['habilitado'])
        return canalesventa

    @staticmethod
    def crear_canalventa (nombre, descripcion, habilitado, user_id=None):
        """
            Función que ingresa un nuevo canal de venta
            Param:
                nombre,
                descripcion,
                habilitado,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                CanalVenta
                None en caso de existir el CanalVenta en la base de datos
        """
        if len(ManagerCanalVenta.obtener_canalesventa(nombre=nombre)) > 0:
            return None
        aux_canalventa = CanalVenta(
            nombre=nombre,
            descripcion=descripcion,
            habilitado=habilitado,
        )
        aux_canalventa.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_canalventa),
                modelo_id=aux_canalventa.id, 
                info={'accion':'creación'}
            )
        return aux_canalventa


    @staticmethod
    def editar_canalventa(canalventa_id, nombre=None, descripcion=None, habilitado=None, user_id=None):
        """
            Función modificar un canal de venta ya ingresado en la base de datos
            Param:
                tipoalojamiento_id
                nombre,
                descripcion,
                habilitado,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                CanalVenta
                None en caso de NO existir el canal de venta en la base de datos
        """
        canalventa = ManagerCanalVenta.obtener_canalventa(canalventa_id)
        if canalventa is None:
            return None
        info = {}
        if nombre:
            if canalventa.nombre != nombre:
                info['nombre'] = canalventa.nombre+' -> '+nombre
                canalventa.nombre = nombre
        if descripcion:
            if canalventa.descripcion != descripcion:
                info['descripcion'] = canalventa.descripcion+' -> '+descripcion
                canalventa.descripcion = descripcion
        if habilitado:
            if canalventa.habilitado != habilitado:
                info['habilitado'] = unicode(canalventa.habilitado)+' -> '+unicode(habilitado)
                canalventa.habilitado = habilitado
        canalventa.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(canalventa),
                modelo_id=canalventa.id, 
                info=info
            )
        return canalventa



class ManagerLog():

    @staticmethod
    def crear_log(user_id, tipo_modelo, modelo_id, info):
        """
            Función para crear un log de Cliente o PotencialCliente
            Params:
                user_id: id del usuario asociado al registro
                tipo_modelo(type): se espera un objeto type del modelo Cliente o PotencialCliente
                modelo_id: id del objeto trabajado
                info: diccionario o lista compatible json
            Returns:
                Log
        """
        log = Log()
        log.user_id = user_id
        if tipo_modelo == type(CanalVenta()):
            log.modelo = Log.CANALVENTA
        if tipo_modelo == type(TipoAlojamiento()):
            log.modelo = Log.TIPOALOJAMIENTO
        if tipo_modelo == type(Alojamiento()):
            log.modelo = Log.ALOJAMIENTO
        if tipo_modelo == type(ReservaAlojamiento()):
            log.modelo = Log.RESERVAALOJAMIENTO
        if tipo_modelo == type(OcupacionAlojamiento()):
            log.modelo = Log.OCUPACIONALOJAMIENTO
        log.modelo_id = modelo_id
        log.info = info
        log.save()
        return log


    @staticmethod
    def obtener_log(log_id):
        """
            Función que obtiene un log especifico
            Param:
                log_id: id del log a buscar
            Return:
                Log
                None en caso de no existir el Log
        """
        try:
            return Log.objects.get(id=log_id)
        except Exception,e:
            return None

    @staticmethod
    def obtener_logs(**kwargs):
        """
            Función para obtener un conjunto de logs según los criterios especificados
            Params:
                user_id(int): id del usuario asociado a los registro
                tipo_modelo(type): se espera un objeto type del modelo Cliente o PotencialCliente
                modelo_id[int]: id de objeto buscados
                modelo_ids[int]: ids del objeto buscados
            QuerySet<Log>
        """
        logs = Log.objects.all()
        if 'user_id' in kwargs:
            logs = logs.filter(user_id__in=kwargs['user_id'])
        if 'tipo_modelo' in kwargs:
            tipo = ''
            if kwargs['tipo_modelo'] == type(CanalVenta()):
                tipo = Log.CANALVENTA
            if kwargs['tipo_modelo'] == type(TipoAlojamiento()):
                tipo = Log.TIPOALOJAMIENTO
            if kwargs['tipo_modelo'] == type(Alojamiento()):
                tipo = Log.ALOJAMIENTO
            if kwargs['tipo_modelo'] == type(ReservaAlojamiento()):
                tipo = Log.RESERVAALOJAMIENTO
            if kwargs['tipo_modelo'] == type(OcupacionAlojamiento()):
                tipo = Log.OCUPACIONALOJAMIENTO
            logs = logs.filter(modelo=tipo)
        if 'modelo_id' in kwargs:
            logs = logs.filter(modelo_id=kwargs['modelo_id'])
        if 'modelo_ids' in kwargs:
            logs = logs.filter(modelo_id__in=kwargs['modelo_ids'])
        return logs


