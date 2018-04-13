# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from models import ReservaAlojamiento, OcupacionAlojamiento, Comentario
from models import LogAlojamiento as Log

from cliente.framework import ManagerCliente
from cliente.empresa.framework import ManagerEmpresa
from framework import ManagerAlojamiento, ManagerCanalVenta, ManagerLog
from alojamiento.tarifa.framework import ManagerTarifa, ManagerTemporada




class ManagerOcupacionAlojamiento():
    """
        Clase para administrar Reserva y ocupacion alojamiento
    """
    ESTADOS_RESERVA = {
        'CONFIRMANDO_PAGO':'confirmando_pago',
        'PAGADA':'pagada',
        'CONFIRMADA':'confirmada',
        'CANCELADA':'cancelada',
    }
    
    @staticmethod
    def obtener_comentario(comentario_id):
        """
            Función que obtiene el Comentario
            Param:
                id: id del comentario
            Return:
                Comentario
                None en caso de no existir el Comentario
        """
        try:
            return Comentario.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_comentarios(**kwargs):
        """
            Función para recuperar los Comentarios
            Param:
                ids
            Return:
                ResultSet<Comentario>
        """
        comentarios = Comentario.objects.all()
        if 'ids' in kwargs:
            comentarios = comentarios.filter(id__in=kwargs['ids'])
        if 'texto' in kwargs:
            comentarios = comentarios.filter(texto=kwargs['texto'])
        return comentarios

    @staticmethod
    def crear_comentario(texto):
        """
            Función que ingresa un nuevo comentario
            Param:
                texto,
            Return:
                Comentario
        """
        aux_comentario = ManagerOcupacionAlojamiento.obtener_comentarios(texto=texto)
        if len(aux_comentario)>0:
            return aux_comentario[0]
        aux_comentario = Comentario(texto=texto)
        aux_comentario.save()
        return aux_comentario

    @staticmethod
    def editar_comentario (comentario_id, texto):
        """
            Función modificar un comentario
            Param:
                comentario_id
                texto
            Return:
                Comentario
                None en caso de NO existir el comentario
        """
        comentario = ManagerOcupacionAlojamiento.obtener_comentario(comentario_id)
        if comentario is None:
            return None
        aux_comentario = ManagerOcupacionAlojamiento.obtener_comentarios(texto=texto)
        if len(aux_comentario)>0:
            return aux_comentario[0]
        comentario.texto = texto
        comentario.save()
        return comentario

    @staticmethod
    def eliminar_comentario(comentario_id):
        """
            Función eliminar un comentario
            Param:
                comentario_id
                texto
            Return:
                Comentario
                None en caso de NO existir el comentario
        """
        comentario = ManagerOcupacionAlojamiento.obtener_comentario(comentario_id)
        if comentario is None:
            return None
        comentario.delete()
        return comentario


    @staticmethod
    def obtener_reservaalojamiento(id):
        """
            Función que obtiene el ReservaAlojamiento
            Param:
                id: id de la ReservaAlojamiento
            Return:
                ReservaAlojamiento
                None en caso de no existir el ReservaAlojamiento
        """
        try:
            return ReservaAlojamiento.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_reservasalojamiento(**kwargs):
        """
            Función para recuperar los ReservaAlojamiento
            Param:
                ids
                estado
                fecha_reservacion_inicio
                fecha_reservacion_final
                cliente_id
                cliente_ids
                empresa_id
                empresa_ids
            Return:
                ResultSet<ReservaAlojamiento>
        """
        reservasalojamiento = ReservaAlojamiento.objects.all()
        if 'ids' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(id__in=kwargs['ids'])
        if 'estado' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(estado=kwargs['estado'])
        if 'fecha_reservacion_inicio' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(fecha_reservacion__gte=kwargs['fecha_reservacion_inicio'])
        if 'fecha_reservacion_final' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(fecha_reservacion__lte=kwargs['fecha_reservacion_final'])
        if 'cliente_id' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(cliente_id=kwargs['cliente_id'])
        if 'cliente_ids' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(cliente_id__in=kwargs['cliente_ids'])
        if 'empresa_id' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(empresa_id=kwargs['empresa_id'])
        if 'empresa_ids' in kwargs:
            reservasalojamiento = reservasalojamiento.filter(empresa_id__in=kwargs['empresa_ids'])
        return tiposalojamiento

    @staticmethod
    def crear_reservaalojamiento(estado, fecha_reservacion, cliente_id, empresa_id, comentario={}, user_id=None):
        """
            Función que ingresa una nueva reserva alojamiento
            Param:
                estado,
                fecha_reservacion,
                cliente_id,
                empresa_id,
                comentario:{key:{codigo_alojamiento:'',comentario:''}},
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                ReservaAlojamiento
                None en caso de existir el reservaalojamiento en la base de datos
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            raise Exception("No existe el cliente.")
        empresa = None
        if empresa_id:
            empresa = ManagerEmpresa.obtener_empresa(empresa_id)
            if empresa is None:
                raise Exception("No existe la empresa.")
        if not ReservaAlojamiento.isEstado(estado):
            raise Exception("Estado incorrecto.")
        aux_reservaalojamiento=ReservaAlojamiento(
            estado=estado,
            fecha_reservacion=fecha_reservacion,
            cliente=cliente,
            empresa=empresa,
        )
        aux_reservaalojamiento.comentario=comentario
        aux_reservaalojamiento.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_reservaalojamiento),
                modelo_id=aux_reservaalojamiento.id, 
                info={'accion':'creación'}
            )
        return aux_reservaalojamiento


    @staticmethod
    def editar_reservaalojamiento (reservaalojamiento_id, estado=None, fecha_reservacion=None, cliente_id=None, empresa_id=None, comentario={}, user_id=None):
        """
            Función modificar una reserva alojamiento
            Param:
                reservaalojamiento_id
                estado,
                fecha_reservacion,
                empresa_id,
                canalventa_id,
                comentario:{key:{codigo_alojamiento:'',comentario:''}},
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                ReservaAlojamiento
                None en caso de NO existir el reserva alojamiento en la base de datos
        """
        reservaalojamiento = ManagerOcupacionAlojamiento.obtener_reservaalojamiento(reservaalojamiento_id)
        if reservaalojamiento is None:
            return None
        info = {}
        if estado:
            if reservaalojamiento.estado != estado:
                info['estado'] = reservaalojamiento.estado+' -> '+estado
                reservaalojamiento.estado = estado
        if fecha_reservacion:
            if reservaalojamiento.fecha_reservacion != fecha_reservacion:
                info['fecha_reservacion'] = unicode(reservaalojamiento.fecha_reservacion)+' -> '+unicode(fecha_reservacion)
                reservaalojamiento.fecha_reservacion = fecha_reservacion
        if cliente_id:
            cliente = ManagerCliente.obtener_cliente(cliente_id)
            if cliente is None:
                raise Exception("No existe el cliente.")
            if reservaalojamiento.cliente != cliente:
                info['cliente'] = unicode(reservaalojamiento.cliente.rut)+' '+unicode(reservaalojamiento.cliente.nombres)+' -> '+unicode(cliente.rut)+' '+unicode(cliente.nombres)
                reservaalojamiento.cliente = cliente
        if empresa_id:
            empresa = ManagerEmpresa.obtener_empresa(empresa_id)
            if empresa is None:
                raise Exception("No existe la empresa.")
            if reservaalojamiento.empresa != empresa:
                info['empresa'] = unicode(reservaalojamiento.empresa.rut)+' '+unicode(reservaalojamiento.empresa.nombre)+' -> '+unicode(empresa.rut)+' '+unicode(empresa.nombre)
                reservaalojamiento.empresa = empresa
        if comentario:
            if reservaalojamiento.comentario != comentario:
                info['comentario'] = unicode(comentario)+' -> '+unicode(comentario)
                reservaalojamiento.comentario = comentario
        reservaalojamiento.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(reservaalojamiento),
                modelo_id=reservaalojamiento.id, 
                info=info
            )
        return reservaalojamiento


    @staticmethod
    def obtener_ocupacionalojamiento(id):
        """
            Función que obtiene la ocupacion alojamiento
            Param:
                id: id de la OcupacionAlojamiento
            Return:
                OcupacionAlojamiento
                None en caso de no existir el OcupacionAlojamiento
        """
        try:
            return OcupacionAlojamiento.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_ocupacionesalojamiento(**kwargs):
        """
            Función para recuperar los OcupacionAlojamiento
            Param:
                ids
                alojamiento_id
                alojamiento_ids
                reservaalojamiento_id
                reservaalojamiento_ids
                fecha
                fecha_inicio
                fecha_final
                canalventa_id
                canalventa_ids
                tarifa_id
                tarifa_ids
            Return:
                ResultSet<OcupacionAlojamiento>
        """
        ocupacionesalojamiento = OcupacionAlojamiento.objects.all()
        if 'ids' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(id__in=kwargs['ids'])
        if 'alojamiento_id' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(alojamiento_id=kwargs['alojamiento_id'])
        if 'alojamiento_ids' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(alojamiento_id__in=kwargs['alojamiento_ids'])
        if 'reservaalojamiento_id' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(reservaalojamiento_id=kwargs['reservaalojamiento_id'])
        if 'reservaalojamiento_ids' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(reservaalojamiento_id__in=kwargs['reservaalojamiento_ids'])
        if 'fecha' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(fecha=kwargs['fecha'])
        if 'fecha_inicio' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(fecha__gte=kwargs['fecha_inicio'])
        if 'fecha_final' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(fecha__lte=kwargs['fecha_final'])
        if 'canalventa_id' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(canalventa_id=kwargs['canalventa_id'])
        if 'canalventa_ids' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(canalventa_id__in=kwargs['canalventa_ids'])
        if 'tarifa_id' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(tarifa_id=kwargs['tarifa_id'])
        if 'tarifa_ids' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(tarifa_id__in=kwargs['tarifa_ids'])
        if 'cautiva' in kwargs:
            ocupacionesalojamiento = ocupacionesalojamiento.filter(cautiva=kwargs['cautiva'])
        return ocupacionesalojamiento

    @staticmethod
    def crear_ocupacionalojamiento(alojamiento_id, reservaalojamiento_id, huespedes, fecha, canalventa_id, tarifa_id, valor, cautiva, user_id=None):
        """
            Función que ingresa una nueva ocupacion alojamiento
            Param:
                alojamiento_id
                reservaalojamiento_id
                huespedes
                fecha
                canalventa_id
                tarifa_id
                valor
                cautiva
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                OcupacionAlojamiento
                None en caso de existir el ocupacionalojamiento en la base de datos
        """
        alojamiento = ManagerAlojamiento.obtener_alojamiento(alojamiento_id)
        if alojamiento is None:
            raise Exception("No existe el alojamiento.")
        reservaalojamiento = ManagerOcupacionAlojamiento.obtener_reservaalojamiento(reservaalojamiento_id)
        if reservaalojamiento is None:
            raise Exception("No existe el reserva alojamiento.")
        canalventa = ManagerCanalVenta.obtener_canalventa(canalventa_id)
        if canalventa is None:
            raise Exception("No existe el canal de venta.")
        tarifa = ManagerTarifa.obtener_tarifa(tarifa_id)
        if tarifa is None:
            raise Exception("No existe el tarifa.")
        if len (ManagerOcupacionAlojamiento.obtener_ocupacionesalojamiento(alojamiento_id=alojamiento_id, fecha=fecha))>0:
            raise Exception("Alojamiento ocupado en la fecha")
        aux_ocupacionalojamiento=OcupacionAlojamiento(
            alojamiento_id=alojamiento_id,
            reservaalojamiento_id=reservaalojamiento_id,
            huespedes=huespedes,
            fecha=fecha,
            canalventa_id=canalventa_id,
            tarifa_id=tarifa_id,
            valor=valor,
            cautiva=cautiva,
        )
        aux_ocupacionalojamiento.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_ocupacionalojamiento),
                modelo_id=aux_ocupacionalojamiento.id, 
                info={'accion':'creación'}
            )
        return aux_ocupacionalojamiento


    @staticmethod
    def editar_ocupacionalojamiento(ocupacionalojamiento_id, alojamiento_id=None, reservaalojamiento_id=None, huespedes=None, fecha=None, canalventa_id=None, tarifa_id=None, valor=None, cautiva=None, user_id=None):
        """
            Función modificar una ocupacion alojamiento
            Param:
                ocupacionalojamiento_id
                alojamiento_id
                reservaalojamiento_id
                huespedes
                fecha
                canalventa_id
                tarifa_id
                valor
                cautiva
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                OcupacionAlojamiento
                None en caso de existir el ocupacionalojamiento en la base de datos
        """
        ocupacionalojamiento = ManagerOcupacionAlojamiento.obtener_ocupacionalojamiento(ocupacionalojamiento_id)
        if ocupacionalojamiento is None:
            return None
        info = {}

        if alojamiento_id:
            if ocupacionalojamiento.alojamiento_id != alojamiento_id:
                alojamiento = ManagerAlojamiento.obtener_alojamiento(alojamiento_id)
                if alojamiento is None:
                    raise Exception("No existe el alojamiento.")
                info['alojamiento'] = ocupacionalojamiento.alojamiento.codigo+' -> '+alojamiento.codigo
                ocupacionalojamiento.alojamiento = alojamiento
        if reservaalojamiento_id:
            if ocupacionalojamiento.reservaalojamiento_id != reservaalojamiento_id:
                reservaalojamiento = ManagerOcupacionAlojamiento.obtener_reservaalojamiento(reservaalojamiento_id)
                if reservaalojamiento is None:
                    raise Exception("No existe el reserva alojamiento.")
                info['reservaalojamiento'] = unicode(ocupacionalojamiento.reservaalojamiento.id)+' -> '+unicode(reservaalojamiento.id)
                ocupacionalojamiento.reservaalojamiento = reservaalojamiento
        if huespedes:
            if ocupacionalojamiento.huespedes != huespedes:
                info['huespedes'] = unicode(ocupacionalojamiento.huespedes)+' -> '+unicode(huespedes)
                ocupacionalojamiento.huespedes = huespedes
        if fecha:
            if ocupacionalojamiento.fecha != fecha:
                info['fecha'] = unicode(ocupacionalojamiento.fecha)+' -> '+unicode(fecha)
                ocupacionalojamiento.fecha = fecha
        if canalventa_id:
            if ocupacionalojamiento.canalventa_id != canalventa_id:
                canalventa = ManagerCanalVenta.obtener_canalventa(canalventa_id)
                if canalventa is None:
                    raise Exception("No existe el canal de venta.")
                info['canalventa'] = unicode(ocupacionalojamiento.canalventa.nombre)+' -> '+unicode(canalventa.nombre)
                ocupacionalojamiento.canalventa = canalventa
        if tarifa_id:
            if ocupacionalojamiento.tarifa_id != tarifa_id:
                tarifa = ManagerTarifa.obtener_tarifa(tarifa_id)
                if tarifa is None:
                    raise Exception("No existe el tarifa.")
                info['tarifa'] = unicode(ocupacionalojamiento.tarifa.id)+':'+ocupacionalojamiento.tarifa.nombre+' -> '+unicode(tarifa.id)+':'+tarifa.nombre
                ocupacionalojamiento.tarifa = tarifa
        if valor:
            if ocupacionalojamiento.valor != valor:
                info['valor'] = unicode(ocupacionalojamiento.valor)+' -> '+unicode(valor)
                ocupacionalojamiento.valor = valor
        if cautiva is not None:
            if ocupacionalojamiento.cautiva != cautiva:
                info['cautiva'] = unicode(ocupacionalojamiento.cautiva)+' -> '+unicode(cautiva)
                ocupacionalojamiento.cautiva = cautiva
        ocupacionalojamiento.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(ocupacionalojamiento),
                modelo_id=ocupacionalojamiento.id, 
                info=info
            )
        return ocupacionalojamiento


    @staticmethod
    def comprobar_ocupacionalojamiento(alojamiento_id, numero_personas, fecha_inicio, fecha_final, cautiva, canalventa_id, tarifa_id):
        """
            Función que comprueba la ocupacion de alojamiento en el rango de fecha
            Params:
                alojamiento_id
                numero_personas
                canalventa_id
                fecha_inicial
                fecha_final
                cautiva
            Return
                Bool, string de con los errores.
        """
        errores = ''
        alojamiento = ManagerAlojamiento.obtener_alojamiento(alojamiento_id)
        if alojamiento is None:
            raise Exception('No existe el alojamiento')
        tipoalojamiento = alojamiento.tipoalojamiento
        canalventa = ManagerCanalVenta.obtener_canalventa(canalventa_id)
        if canalventa is None:
            raise Exception('No existe el canal de venta')
        tarifa = ManagerTarifa.obtener_tarifa(tarifa_id)
        if tarifa is None:
            raise Exception('No existe la tarifa.')
        if tipoalojamiento.capacidad < numero_personas:
            errores += 'El número de personas, excede el límite del tipo de alojamiento ['+unicode(tipoalojamiento.capacidad)+'], '
        if fecha_inicio > fecha_final:
            errores += 'La fecha inicial es mayor a la final'
        else:
            aux_ocupaciones = ManagerOcupacionAlojamiento.obtener_ocupacionesalojamiento(alojamiento_id=alojamiento.id,fecha_inicio=fecha_inicio, fecha_final=fecha_final)
            if len(aux_ocupaciones) > 0:
                errores += 'El alojamiento se encuentra ocupado en los siguientes días '
                for ocupacion in aux_ocupaciones:
                    errores += unicode(ocupacion.fecha)+', '
        aux_temporadasfecha = ManagerTemporada.obtener_temporadasfecha(fecha_inicio=fecha_inicio, fecha_final=fecha_final)
        aux_temporadasfecha = aux_temporadasfecha.values('temporada_id').distinct()
        if len(aux_temporadasfecha) > 1 :
            errores += 'Las fechas no pueden pertenecer a temporadas diferentes'
        return True if errores == '' else False, errores

