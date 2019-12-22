# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from models import Temporada, TemporadaFecha, Tarifa
from models import LogTarifa as Log

from alojamiento.framework import ManagerAlojamiento, ManagerCanalVenta
from cliente.empresa.framework import ManagerEmpresa
from cliente.framework import ManagerCliente
from common import utils as utils_common

class ManagerTemporada():
    """
        Clase para administrar las Temporadas
    """
    @staticmethod
    def obtener_temporada(id):
        """
            Función que obtiene el temporada
            Param:
                id: id de la temporada
            Return:
                Temporada
                None en caso de no existir el temporada
        """
        try:
            return Temporada.objects.get(id=id)
        except Exception,e:
            return None

    @staticmethod
    def obtener_temporadas(**kwargs):
        """
            Función para recuperar las temporadas
            Param:
                nombre
            Return:
                ResultSet<Temporada>
                
        """
        temporadas = Temporada.objects.all()
        if 'ids' in kwargs:
            temporadas = temporadas.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            temporadas = temporadas.filter(nombre=kwargs['nombre'])
        return temporadas


    @staticmethod
    def crear_temporada(nombre, descripcion, user_id=None):
        """
            Función para ingresar una nueva temporada
            Params:
                nombre: nombre de la temporada
                descripcion: descripcion de la temporada
                user_id(opcional): usuario creador de la temporada
            Return:
                Temporada
                None si la temporada ya ha sido creada, nombre repetido
        """
        temporadas = ManagerTemporada.obtener_temporadas(nombre=nombre)
        if len(temporadas) > 0:
            return None
        aux_temporada = Temporada(
            nombre=nombre,
            descripcion=descripcion,
        )
        aux_temporada.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_temporada),
                modelo_id=aux_temporada.id, 
                info={'accion':'creación'}
            )
        return aux_temporada


    @staticmethod
    def editar_temporada(temporada_id,nombre=None, descripcion=None, user_id=None):
        """
            Función para editar temporada
            Params:
                temporada_id: id de la temporada
                nombre: nombre de la temporada
                descripcion: descripción de la temporada
                user_id: opcional para Log
            Return:
                Temporada
                None en caso de NO existir la tempraoda en la base de datos
        """
        temporada = ManagerTemporada.obtener_temporada(temporada_id)
        if temporada is None:
            return None
        info = {}
        if nombre:
            if temporada.nombre != nombre:
                info['nombre'] = temporada.nombre,' -> ',nombre
                temporada.nombre = nombre
        if descripcion:
            if temporada.descripcion != descripcion:
                info['descripcion'] = temporada.descripcion,' -> ',descripcion
                temporada.descripcion = descripcion
        temporada.save()
        if user_id:
            info['accion']=u'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(temporada),
                modelo_id=temporada.id, 
                info=info
            )
        return temporada


    @staticmethod
    def obtener_temporadafecha(**kwargs):
        """
            Función para obtener la temporada correspondiente a la id o la fecha
            Params:
                id
                fecha
            Returns:
                TemporadaFecha
                None, si no existe
        """
        try:
            if 'id' in kwargs:
                return TemporadaFecha.objects.get(id=kwargs['id'])
            if 'fecha' in kwargs:
                return TemporadaFecha.objects.get(fecha=kwargs['fecha'])
            return None
        except Exception,e:
            return None

    @staticmethod
    def obtener_temporadasfecha(**kwargs):
        """
            Función para obtener la temporada correspondiente a la id o la fecha
            Params:
                ids
                fecha_inicio
                fecha_final
                temporada_id
                temporada_ids
            Returns:
                QuerySet<TemporadaFecha>
        """
        temporadafechas = TemporadaFecha.objects.all()
        if 'ids' in kwargs:
            temporadafechas = temporadafechas.filter(id__in=kwargs['ids'])
        if 'fecha_inicio' in kwargs:
            temporadafechas = temporadafechas.filter(fecha__gte=kwargs['fecha_inicio'])
        if 'fecha_final' in kwargs:
            temporadafechas = temporadafechas.filter(fecha__lte=kwargs['fecha_final'])
        if 'temporada_id' in kwargs:
            temporadafechas = temporadafechas.filter(temporada_id=kwargs['temporada_id'])
        if 'temporada_ids' in kwargs:
            temporadafechas = temporadafechas.filter(temporada_id__in=kwargs['temporada_ids'])
        return temporadafechas

    @staticmethod
    def insertar_fechatemporada(fecha, temporada_id):
        """
            Función para insertar la temporada correspondiente a la fecha
            Params:
                fecha
                temporada_id
            Returns:
                TemporadaFecha
                None en caso de error
        """
        temporada = ManagerTemporada.obtener_temporada(id=temporada_id)
        if temporada is None:
            return None
        temporadafecha = ManagerTemporada.obtener_temporadafecha(fecha=fecha)
        if temporadafecha is None:
            temporadafecha = TemporadaFecha(fecha=fecha)
        temporadafecha.temporada = temporada
        temporadafecha.save()
        return temporadafecha


class ManagerTarifa():
    
    @staticmethod
    def obtener_tarifa(id):
        """
            Función que obtiene la tarifa
            Param:
                id: id de la tarifa
            Return:
                Tarifa
                None en caso de no existir el tarifa
        """
        try:
            return Tarifa.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_tarifas(**kwargs):
        """
            Función que obtiene las tarifas
            Param:
                ids: id de la tarifa
                nombre: nombre de la tarifa
            Return:
                Tarifa
                None en caso de no existir el tarifa
        """
        tarifas = Tarifa.objects.all()
        if 'ids' in kwargs:
            tarifas = tarifas.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            tarifas = tarifas.filter(nombre=kwargs['nombre'])
        return tarifas


    @staticmethod
    def crear_tarifa(nombre, descripcion, habilitado, restricciones, valores, user_id=None):
        """
            Función para ingresar una nueva tarifa
            Params:
                nombre: nombre de la temporada
                descripcion: descripcion de la temporada
                habilitado
                restricciones{
                    temporadas:[temporadas_id,,],
                    canales_venta:[canal_venta_id,,,],
                    tipos_alojamiento:[tipo_alojamiento_id,,],
                    empresas:[int,,,,,],
                }: diccionario con las restricciones a utilizar en la tarifa 
                valores {
                    dia_bdd:{
                    n_personas:$valor,
                    },....
                }
                user_id(opcional): usuario creador de la temporada
            Return:
                Tarifa
                None si el nombre de la tarifa ya ha sido creada, nombre repetido
        """
        tarifa = ManagerTarifa.obtener_tarifas(nombre=nombre)
        if len(tarifa) > 0:
            return None
        restricciones_check, restricciones_errores = ManagerTarifa.comprobar_restricciones(restricciones)
        if not restricciones_check:
            print restricciones_errores
            return None
        valores_check, valores_errores = ManagerTarifa.comprobar_valores(valores)
        if not valores_check:
            print valores_errores
            return None
        restricciones['meta_dias'] = utils_common.generar_diccionario_dias([1,2,3,4,5,6,7], 'bdd')
        if not 'temporadas' in restricciones:
            restricciones['temporadas'] = []
        if not 'canales_venta' in restricciones:
            restricciones['canales_venta'] = []
        if not 'tipos_alojamiento' in restricciones:
            restricciones['tipos_alojamiento'] = []
        if not 'empresas' in restricciones:
            restricciones['empresas'] = []
        aux_tarifa = Tarifa(
            nombre=nombre,
            descripcion=descripcion,
            habilitado=habilitado,
            restricciones=restricciones,
            valores=valores,
        )
        aux_tarifa.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_tarifa),
                modelo_id=aux_tarifa.id, 
                info={'accion':'creación'}
            )
        return aux_tarifa


    @staticmethod
    def editar_tarifa(tarifa_id, nombre=None, descripcion=None, habilitado=None, restricciones=None, valores=None, user_id=None):
        """
            Función para editar una tarifa
            Params:
                nombre: nombre de la temporada
                descripcion: descripcion de la temporada
                habilitado
                restricciones{
                    temporadas:[temporadas_id,,],
                    canales_venta:[canal_venta_id,,,],
                    tipos_alojamiento:[tipo_alojamiento_id,,],
                    empresas:[int,,,,,],
                }: diccionario con las resticciones a utilizar en la tarifa 
                valores {
                    dia_bdd:{
                    n_personas:$valor,
                    },....
                }
                user_id(opcional): usuario creador de la temporada
            Return:
                Tarifa
                None en caso de NO existir la tarifa en la base de datos
        """
        tarifa = ManagerTarifa.obtener_tarifa(tarifa_id)
        if tarifa is None:
            return None
        info = {}
        if nombre:
            if tarifa.nombre != nombre:
                info['nombre'] = tarifa.nombre,' -> ',nombre
                tarifa.nombre = nombre
        if descripcion:
            if tarifa.descripcion != descripcion:
                info['descripcion'] = tarifa.descripcion,' -> ',descripcion
                tarifa.descripcion = descripcion
        if habilitado:
            if tarifa.habilitado != habilitado:
                info['habilitado'] = tarifa.habilitado+' -> '+habilitado
                tarifa.habilitado = habilitado
        if restricciones:
            if tarifa.restricciones != restricciones:
                restricciones_check, restricciones_errores = ManagerTarifa.comprobar_restricciones(restricciones)
                if not restricciones_check:
                    print restricciones_errores
                    return None
                restricciones['meta_dias'] = utils_common.generar_diccionario_dias([1,2,3,4,5,6,7], 'bdd')
                info['restricciones'] = unicode(tarifa.restricciones)+' -> '+unicode(restricciones)
                tarifa.restricciones = restricciones
        if valores:
            if tarifa.valores != valores:
                valores_check, valores_errores = ManagerTarifa.comprobar_valores(valores)
                if not valores_check:
                    print valores_errores
                    return None
                info['valores'] = unicode(tarifa.valores)+' -> '+unicode(valores)
                tarifa.valores = valores
        aux_restricciones = tarifa.restricciones
        if not 'temporadas' in aux_restricciones:
            aux_restricciones['temporadas'] = []
        if not 'canales_venta' in aux_restricciones:
            aux_restricciones['canales_venta'] = []
        if not 'tipos_alojamiento' in aux_restricciones:
            aux_restricciones['tipos_alojamiento'] = []
        if not 'empresas' in aux_restricciones:
            aux_restricciones['empresas'] = []
        tarifa.restricciones = aux_restricciones
        tarifa.save()
        if user_id:
            info['accion']=u'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(tarifa),
                modelo_id=tarifa.id, 
                info=info
            )
        return tarifa


    @staticmethod
    def comprobar_restricciones(restricciones):
        """
            Función para chequear la correcta implementacion de las restricciones
            Params:
                restricciones{
                    temporadas:[temporadas_id,,],
                    canales_venta:[canal_venta_id,,,],
                    tipos_alojamiento:[tipo_cabanas_id,,],
                    empresas:[int,,,,,],
                }: diccionario con las resticciones a utilizar en la tarifa 
            Return:
                bool, error : True si cumple con los requisitos, False en caso contrario
        """
        flag = True
        if type(restricciones) != type({}):
            return False, ' No es un diccionario'
        keys_restricciones = ['temporadas', 'canales_venta', 'tipos_alojamiento', 'empresas']
        for key in restricciones:
            if not key in keys_restricciones:
                return False, 'Key '+unicode(key)+' No esta en las restricciones'
            if key == 'temporadas':
                if type(restricciones[key]) != type([]):
                    return False, ' Temporadas no es un array'
                temporadas = ManagerTemporada.obtener_temporadas(ids=restricciones[key])
                if len(restricciones[key]) != len(temporadas):
                    print restricciones[key], temporadas.__dict__
                    return False, ' Problemas con las keys de temporadas'
            elif key == 'tipos_alojamiento':
                if type(restricciones[key]) != type([]):
                    return False, ' tipos de alojamiento no es un array'
                tipos_cabana = ManagerAlojamiento.obtener_tiposalojamiento(ids=restricciones[key])
                if len(restricciones[key]) != len(tipos_cabana):
                    return False, ' Problemas con las key de tipos de alojamiento'
            elif key == 'empresas':
                if type(restricciones[key]) != type([]):
                    return False, ' Empresas no es un array'
                empresas = ManagerEmpresa.obtener_empresas(ids=restricciones[key])
                if len(restricciones[key]) != len(empresas):
                    return False, ' Problemas con las key de empresas'
            elif key == 'canales_venta':
                if type(restricciones[key]) != type([]):
                    return False, ' Canales venta no es un array'
                canales_venta = ManagerCanalVenta.obtener_canalesventa(ids=restricciones[key])
                if len(restricciones[key]) != len(canales_venta):
                    return False, ' Problemas con las key de canales venta'
        return True, None


    @staticmethod
    def comprobar_valores(valores):
        """
            Función para chequear la correcta implementacion de los valores
            Params:
                valores {
                    dia_bdd:{
                    n_personas:$valor,
                    },....
                }
            Return:
                bool, error : True si cumple con los requisitos, False en caso contrario
        """
        flag = True
        if type(valores) != type({}):
            return False, ' No es un diccionario'
        for key in valores:
            if type(key) != type(1):
                return False, ' La key no es un entero'
            if key < 1 or key > 7:
                return False, ' La key no esta dentro de los días bdd'
            if type(valores[key]) != type({}):
                return False, 'valores[key] No es un diccionario'
            for key_2 in valores[key]:
                if type(key_2) != type(1):
                    return False, ' La key_2 no es un entero'
                if not ((type(valores[key][key_2]) == type(1)) or (type(valores[key][key_2]) == type(1.1))):
                    return False, ' El valor tiene que ser entero o float'
        return True, None


    @staticmethod
    def comprobar_tarifa_valida(tarifa_id, cliente_id, tipoalojamiento_id, canalventa_id, temporada_id ):
        """
            Función para comprobar la validez de la tarifa para el cliente especifico, según los parametros
            params:
                temporadas:[temporadas_id,,],
                canales_venta:[canal_venta_id,,,],
                tipos_alojamiento:[tipo_alojamiento_id,,],
                empresas:[int,,,,,],
            Return:
                Bool, errores
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            raise Exception('No existe el cliente.')
        empresas = ManagerEmpresa.obtener_asociacionclienteempresa(cliente_id=cliente.id)
        tarifa = ManagerTarifa.obtener_tarifa(tarifa_id)
        if tarifa is None:
            raise Exception('No existe el tarifa.')
        restricciones = tarifa.restricciones
        errores = ''
        if not tarifa.habilitado:
            errores += 'La tarifa no esta habilitada. '
        if len(restricciones['temporadas']) > 0:
            if not temporada_id in restricciones['temporadas']:
                errores += 'La tarifa no es aplicable en la temporada. '
        if len(restricciones['canales_venta']) > 0:
            if not canalventa_id in restricciones['canales_venta']:
                errores += 'La tarifa no es aplicable en la canal de venta. '
        if len(restricciones['tipos_alojamiento']) > 0:
            if not tipoalojamiento_id in restricciones['tipos_alojamiento']:
                errores += 'La tarifa no es aplicable a este tipo de alojamiento. '
        if len(restricciones['empresas']) > 0:
            flag = False
            for empresa in empresas:
                if empresa.id in restricciones['empresas']:
                    flag = True
            if not flag:
                errores += 'La tarifa es aplicable solo a ciertas empresas. '
        return True if errores == '' else False, errores


class ManagerLog():

    @staticmethod
    def crear_log(user_id, tipo_modelo, modelo_id, info):
        """
            Función para crear un log de Temporada, TemporadaFecha, Tarifa
            Params:
                user_id: id del usuario asociado al registro
                tipo_modelo(type): se espera un objeto type del modelo Temporada, TemporadaFecha o Tarifa
                modelo_id: id del objeto trabajado
                info: diccionario o lista compatible json
            Returns:
                Log
        """
        log = Log()
        log.user_id = user_id
        if tipo_modelo == type(Temporada()):
            log.modelo = Log.TEMPORADA
        if tipo_modelo == type(TemporadaFecha()):
            log.modelo = Log.TEMPORADA_FECHA
        if tipo_modelo == type(Tarifa()):
            log.modelo = Log.TARIFA
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
                tipo_modelo(type): se espera un objeto type del modelo Temporada, TemporadaFecha o Tarifa
                modelo_id[int]: id de objeto buscados
                modelo_ids[int]: ids del objeto buscados
            QuerySet<Log>
        """
        logs = Log.objects.all()
        if 'user_id' in kwargs:
            logs = logs.filter(user_id__in=kwargs['user_id'])
        if 'tipo_modelo' in kwargs:
            tipo = ''
            if kwargs['tipo_modelo'] == type(Temporada()):
                tipo = Log.TEMPORADA
            if kwargs['tipo_modelo'] == type(TemporadaFecha()):
                tipo = Log.TEMPORADA_FECHA
            if kwargs['tipo_modelo'] == type(Tarifa()):
                tipo = Log.TARIFA
            logs = logs.filter(modelo=tipo)
        if 'modelo_id' in kwargs:
            logs = logs.filter(modelo_id=kwargs['modelo_id'])
        if 'modelo_ids' in kwargs:
            logs = logs.filter(modelo_id__in=kwargs['modelo_ids'])
        return logs