# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from models import Empresa, AsociacionClienteEmpresa
from cliente.framework import ManagerLog, ManagerCliente



class ManagerEmpresa():
    """
        Clase para las Empresas
    """
    @staticmethod
    def obtener_empresa(id):
        """
            Función que obtiene el empresa
            Param:
                id: id de la empresa
            Return:
                Empresa
                None en caso de no existir el Empresa
        """
        try:
            return Empresa.objects.get(id=id)
        except Exception,e:
            return None


    @staticmethod
    def obtener_empresas(**kwargs):
        """
            Función para recuperar las empresas
            Param:
                nombre
            Return:
                ResultSet<Empresa>
                
        """
        empresas = Empresa.objects.all()
        if 'ids' in kwargs:
            empresas = empresas.filter(id__in=kwargs['ids'])
        if 'nombre' in kwargs:
            empresas = empresas.filter(nombre=kwargs['nombre'])
        if 'rut' in kwargs:
            empresas = empresas.filter(rut=kwargs['rut'])
        if 'ciudad' in kwargs:
            empresas = empresas.filter(rut=kwargs['ciudad'])
        return empresas


    @staticmethod
    def crear_empresa(nombre, rut, digito_verificador, telefono, direccion, ciudad, email, descripcion='', user_id=None):
        """
            Función que ingresa un nuevo cliente
            Param:
                nombre=nombre,
                rut=rut,
                digito_verificador=digito_verificador,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                email=email,
                descripcion=descripcion,
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                Cliente
                None en caso de existir el cliente en la base de datos
        """
        if len(ManagerEmpresa.obtener_empresas(rut=rut)) > 0:
            return None
        aux_empresa = Empresa(
            nombre=nombre,
            rut=rut,
            digito_verificador=digito_verificador,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            email=email,
            descripcion=descripcion,
        )
        aux_empresa.save()
        if user_id:
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(aux_empresa),
                modelo_id=aux_empresa.id, 
                info={'accion':'creación'}
            )
        return aux_empresa


    @staticmethod
    def editar_empresa(empresa_id, nombre, rut, digito_verificador, telefono, direccion, ciudad, email, descripcion='', user_id=None):
        """
            Función para editar un empresa ya ingresado en la base de datos
            Param:
                empresa_id = id del cliente a editar
                nombre
                rut
                digito_verificador
                telefono
                direccion
                ciudad
                email
                descripcion
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                Empresa
                None en caso de NO existir el empresa en la base de datos
        """
        empresa = ManagerEmpresa.obtener_empresa(empresa_id)
        if empresa is None:
            return None
        info = {}
        if nombre:
            if empresa.nombre != nombre:
                info['nombre'] = empresa.nombre+' -> '+nombre
                empresa.nombre = nombre
        if rut:
            if empresa.rut != rut:
                info['rut'] = empresa.rut,' -> ',rut
                empresa.rut = rut
        if digito_verificador:
            if empresa.digito_verificador != digito_verificador:
                info['digito_verificador'] = empresa.digito_verificador,' -> ',digito_verificador
                empresa.digito_verificador = digito_verificador
        if telefono:
            if empresa.telefono != telefono:
                info['telefono'] = empresa.telefono+' -> '+telefono
                empresa.telefono = telefono
        if direccion:
            if empresa.direccion != direccion:
                info['direccion'] = empresa.direccion+' -> '+direccion
                empresa.direccion = direccion
        if ciudad:
            if empresa.ciudad != ciudad:
                info['ciudad'] = empresa.ciudad+' -> '+ciudad
                empresa.ciudad = ciudad
        if email:
            if empresa.email != email:
                info['email'] = empresa.email+' -> '+email
                empresa.email = email
        if descripcion:
            if empresa.descripcion != descripcion:
                info['descripcion'] = empresa.descripcion+' -> '+descripcion
                empresa.descripcion = descripcion
        empresa.save()
        if user_id:
            info['accion']=u'modificación'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(empresa),
                modelo_id=empresa.id,
                info=info
            )
        return empresa


    @staticmethod
    def obtener_asociacionclienteempresa (**kwargs):
        """
            Función para recuperar las asociaciones cliente empresa
            Params:
                cliente_id: id del cliente buscados
                empresa_id: id de la empresa 
            Returns:
                ResultSet<AsociacionClienteEmpresa>
        """
        asociacionesclienteempresa = AsociacionClienteEmpresa.objects.all()
        if 'cliente_id' in kwargs:
            asociacionesclienteempresa = asociacionesclienteempresa.filter(cliente_id=kwargs['cliente_id'])
        if 'empresa_id' in kwargs:
            asociacionesclienteempresa = asociacionesclienteempresa.filter(empresa_id=kwargs['empresa_id'])
        return asociacionesclienteempresa

    @staticmethod
    def asociar_cliente_empresa (cliente_id, empresa_id, user_id):
        """
            Función para asociar un cliente a una empresa
            Param:
                cliente_id = id del cliente a editar
                empresa_id = id de la empresa
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                AsociacionClienteEmpresa
                None en caso de NO existir el cliente o empresa en la base de datos
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            return None
        empresa = ManagerEmpresa.obtener_empresa(empresa_id)
        if empresa is None:
            return None
        asociacionesclienteempresa = ManagerEmpresa.obtener_asociacionclienteempresa(cliente_id=cliente_id,empresa_id=empresa_id)
        if len(asociacionesclienteempresa) > 0:
            return asociacionesclienteempresa[0]
        asociacionclienteempresa = AsociacionClienteEmpresa(
            cliente=cliente,
            empresa=empresa,
        )
        asociacionclienteempresa.save()
        if user_id:
            info={
                'accion':u'asociación a empresa',
                'empresa':empresa.nombre,
                'asoc_id':asociacionclienteempresa.id,
            }
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(cliente),
                modelo_id=cliente.id,
                info=info,
            )
            info={
                'accion':u'asociación de cliente',
                'cliente':cliente.nombres+' '+cliente.apellidos,
                'asoc_id':asociacionclienteempresa.id,
            }
            info['accion']=u'asociación de cliente'
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(empresa),
                modelo_id=empresa.id,
                info=info,
            )
        return asociacionclienteempresa


    @staticmethod
    def desasociar_cliente_empresa (cliente_id, empresa_id, user_id):
        """
            Función para asociar un cliente a una empresa
            Param:
                cliente_id = id del cliente a editar
                empresa_id = id de la empresa
                user_id: si el usuario esta seteado se creara un log asociado a él
            Return:
                Boolean
                None en caso de error
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            return None
        empresa = ManagerEmpresa.obtener_empresa(empresa_id)
        if empresa is None:
            return None
        asociacionesclienteempresa = ManagerEmpresa.obtener_asociacionclienteempresa(cliente_id=cliente_id, empresa_id=empresa_id)
        if len(asociacionesclienteempresa) == 0:
            return True
        asociacionesclienteempresa[0].delete()
        if user_id:
            info={
                'accion':u'desasociación de empresa',
                'empresa':empresa.nombre,
            }
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(cliente),
                modelo_id=cliente.id,
                info=info,
            )
            info={
                'accion':u'desasociación de cliente',
                'cliente':cliente.nombres+' '+cliente.apellidos
            }
            ManagerLog.crear_log(
                user_id=user_id,
                tipo_modelo=type(empresa),
                modelo_id=empresa.id,
                info=info,
            )
        return True