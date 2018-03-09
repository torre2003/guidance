# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from cliente.models import Cliente, PotencialCliente
from cliente.models import LogCliente as Log
from cliente.empresa.models import Empresa


class ManagerCliente():
    """
        Clase para administrar los clientes
    """


    @staticmethod
    def obtener_cliente(id):
        """
            Función que obtiene el cliente
            Param:
                id: id del cliente 
            Return:
                Cliente
                None en caso de no existir el cliente
        """
        try:
            return Cliente.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_cliente_por_rut(rut):
        """
            Función que obtiene el cliente según rut
            Param:
                rut: rut sin digito verificador
            Return:
                Cliente
                None en caso de no existir el cliente
        """
        try:
            return Cliente.objects.get(rut=rut)
        except Exception,e:
            return None


    @staticmethod
    def obtener_clientes():
        """
            Función que los clientes ingresados en el sistema
            Param:
            Return:
                ResultSet<Cliente>
                
        """
        clientes = Cliente.objects.all()
        return clientes

    
    # _ANS = obtener_cliente_por_rut.__func__()  # call the staticmethod


    @staticmethod
    def crear_cliente (nombres, apellidos, direccion, ciudad, pais, email, sexo, telefono, rut,
                    digito_verificador, fecha_nacimiento = None, descripcion='', user_id=None):
        """
            Función que ingresa un nuevo cliente
            Param:
                nombres=nombres,
                apellidos=apellidos,
                direccion=direccion,
                ciudad=ciudad,
                pais=pais,
                email=email,
                sexo=sexo,
                telefono=telefono,
                rut=rut,
                digito_verificador=digito_verificador,
                descripcion=descripcion,
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                Cliente
                None en caso de existir el cliente en la base de datos
        """
        if ManagerCliente.obtener_cliente_por_rut(rut) is not None:
            return None
        aux_cliente = Cliente(
            nombres=nombres,
            apellidos=apellidos,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            ciudad=ciudad,
            pais=pais,
            email=email,
            sexo=sexo,
            telefono=telefono,
            rut=rut,
            digito_verificador=digito_verificador,
            descripcion=descripcion,
        )
        aux_cliente.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_cliente),
                modelo_id=aux_cliente.id, 
                info={'accion':'creación'}
            )
        return aux_cliente


    @staticmethod
    def editar_cliente (cliente_id, rut=None, digito_verificador=None, nombres=None, apellidos=None,
                        direccion=None, ciudad=None, pais=None, email=None, sexo=None, telefono=None,
                        fecha_nacimiento = '', descripcion=None, user_id=None):
        """
            Función para editar un cliente ya ingresado en la base de datos
            Param:
                cliente_id = id del cliente a editar
                rut
                digito_verificador
                nombres
                apellidos
                direccion
                ciudad
                pais
                email
                sexo
                telefono
                fecha_nacimiento
                descripcion
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                Cliente
                None en caso de NO existir el cliente en la base de datos
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            return None
        info = {}
        if rut:
            if cliente.rut != rut:
                info['rut'] = cliente.rut,' -> ',rut
                cliente.rut = rut
        if digito_verificador:
            if cliente.digito_verificador != digito_verificador:
                info['digito_verificador'] = cliente.digito_verificador,' -> ',digito_verificador
                cliente.digito_verificador = digito_verificador
        if nombres:
            if cliente.nombres != nombres:
                info['nombres'] = cliente.nombres+' -> '+nombres
                cliente.nombres = nombres
        if apellidos:
            if cliente.apellidos != apellidos:
                info['apellidos'] = cliente.apellidos+' -> '+apellidos
                cliente.apellidos = apellidos
        if direccion:
            if cliente.direccion != direccion:
                info['direccion'] = cliente.direccion+' -> '+direccion
                cliente.direccion = direccion
        if ciudad:
            if cliente.ciudad != ciudad:
                info['ciudad'] = cliente.ciudad+' -> '+ciudad
                cliente.ciudad = ciudad
        if pais:
            if cliente.pais != pais:
                info['pais'] = cliente.pais+' -> '+pais
                cliente.pais = pais
        if email:
            if cliente.email != email:
                info['email'] = cliente.email+' -> '+email
                cliente.email = email
        if sexo:
            if cliente.sexo != sexo:
                info['sexo'] = cliente.sexo+' -> '+sexo
                cliente.sexo = sexo
        if telefono:
            if cliente.telefono != telefono:
                info['telefono'] = cliente.telefono+' -> '+telefono
                cliente.telefono = telefono
        if fecha_nacimiento != '':
            if cliente.fecha_nacimiento != fecha_nacimiento:
                info['fecha_nacimiento'] = unicode(cliente.fecha_nacimiento)+' -> '+unicode(fecha_nacimiento)
                cliente.fecha_nacimiento = fecha_nacimiento
        if descripcion:
            if cliente.descripcion != descripcion:
                info['descripcion'] = cliente.descripcion+' -> '+descripcion
                cliente.descripcion = descripcion
        cliente.save()
        if user_id:
            info['accion']=u'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(cliente),
                modelo_id=cliente.id, 
                info=info
            )
        return cliente

class ManagerPotencialCliente():
    """
        Clase para administrar potenciales clientes
    """

    @staticmethod
    def obtener_potencial_cliente(id):
        """
            Función que obtiene el potencial cliente
            Param:
                id: id del potencial cliente 
            Return:
                PotencialCliente
                None en caso de no existir el potencial cliente
        """
        try:
            return PotencialCliente.objects.get(id=id)
        except Exception,e:
            return None

    @staticmethod
    def obtener_potenciales_clientes():
        """
            Función que retorna los potenciales clientes ingresados en el sistema
            Param:
            Return:
                ResultSet<PotencialCliente>
                
        """
        potenciales_clientes = PotencialCliente.objects.all()
        return potenciales_clientes


    @staticmethod
    def crear_potencial_cliente (nombre_completo, email, telefono, nacionalidad, descripcion, user_id=None):
        """
            Función que ingresa un nuevo potencial cliente
            Param:
                nombre_completo=nombre_completo,
                email=email,
                telefono=telefono,
                nacionalidad=nacionalidad,
                descripcion=descripcion,
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                PotencialCliente
                None en caso de existir el cliente en la base de datos
        """
        aux_potencial_cliente = PotencialCliente(
            nombre_completo=nombre_completo,
            email=email,
            telefono=telefono,
            nacionalidad=nacionalidad,
            descripcion=descripcion
        )
        aux_potencial_cliente.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_potencial_cliente),
                modelo_id=aux_potencial_cliente.id, 
                info={'accion':'creación'}
            )
        return aux_potencial_cliente


    @staticmethod
    def editar_potencial_cliente (potencial_cliente_id, nombre_completo=None, email=None, telefono=None, nacionalidad=None, descripcion=None, user_id=None):
        """
            Función modificar un potencial cliente ya ingresado en la base de datos
            Param:
                potencial_cliente_id = id del cliente a editar
                nombre_completo(Opcional)
                email(Opcional)
                telefono(Opcional)
                nacionalidad(Opcional)
                descripcion(Opcional)
                user_id(Opcional): si se especifica la id de usuario, se creara un Log asociada a él
            Return:
                PotencialCliente
                None en caso de NO existir el potencial cliente en la base de datos
        """
        potencial_cliente = ManagerPotencialCliente.obtener_potencial_cliente(potencial_cliente_id)
        if potencial_cliente is None:
            return None
        info = {}
        if nombre_completo:
            if potencial_cliente.nombre_completo != nombre_completo:
                info['nombre_completo'] = potencial_cliente.nombre_completo+' -> '+nombre_completo
                potencial_cliente.nombre_completo = nombre_completo
        if email:
            if potencial_cliente.email != email:
                info['email'] = potencial_cliente.email+' -> '+email
                potencial_cliente.email = email
        if telefono:
            if potencial_cliente.telefono != telefono:
                info['telefono'] = potencial_cliente.telefono+' -> '+telefono
                potencial_cliente.telefono = telefono
        if nacionalidad:
            if potencial_cliente.nacionalidad != nacionalidad:
                info['nacionalidad'] = potencial_cliente.nacionalidad+' -> '+nacionalidad
                potencial_cliente.nacionalidad = nacionalidad
        if descripcion:
            if potencial_cliente.descripcion != descripcion:
                info['descripcion'] = potencial_cliente.descripcion+' -> '+descripcion
                potencial_cliente.descripcion = descripcion
        potencial_cliente.save()
        if user_id:
            info['accion'] = 'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(potencial_cliente),
                modelo_id=potencial_cliente.id, 
                info=info
            )
        return potencial_cliente


class ManagerLog():

    @staticmethod
    def crear_log(user_id, tipo_modelo, modelo_id, info):
        """
            Función para crear un log de Cliente, PotencialCliente, Empresa
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
        if tipo_modelo == type(Cliente()):
            log.modelo = Log.CLIENTE
        if tipo_modelo == type(PotencialCliente()):
            log.modelo = Log.POTENCIAL_CLIENTE
        if tipo_modelo == type(Empresa()):
            log.modelo = Log.EMPRESA
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
            if kwargs['tipo_modelo'] == type(Cliente()):
                tipo = Log.CLIENTE
            if kwargs['tipo_modelo'] == type(PotencialCliente()):
                tipo = Log.POTENCIAL_CLIENTE
            if kwargs['tipo_modelo'] == type(Empresa()):
                tipo = Log.EMPRESA
            logs = logs.filter(modelo=tipo)
        if 'modelo_id' in kwargs:
            logs = logs.filter(modelo_id=kwargs['modelo_id'])
        if 'modelo_ids' in kwargs:
            logs = logs.filter(modelo_id__in=kwargs['modelo_ids'])
        return logs