# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from cliente.models import Cliente, PotencialCliente



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
    def crear_cliente (nombres, apellidos, direccion, ciudad, pais, email, sexo, telefono, rut, digito_verificador, fecha_nacimiento = None, descripcion=''):
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
        return aux_cliente


    @staticmethod
    def editar_cliente (cliente_id, rut=None, digito_verificador=None, nombres=None, apellidos=None, direccion=None, ciudad=None, pais=None, email=None, sexo=None, telefono=None, fecha_nacimiento = '', descripcion=None):
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
            Return:
                Cliente
                None en caso de NO existir el cliente en la base de datos
        """
        cliente = ManagerCliente.obtener_cliente(cliente_id)
        if cliente is None:
            return None
        if rut:
            cliente.rut = rut
        if digito_verificador:
            cliente.digito_verificador = digito_verificador
        if nombres:
            cliente.nombres = nombres
        if apellidos:
            cliente.apellidos = apellidos
        if direccion:
            cliente.direccion = direccion
        if ciudad:
            cliente.ciudad = ciudad
        if pais:
            cliente.pais = pais
        if email:
            cliente.email = email
        if sexo:
            cliente.sexo = sexo
        if telefono:
            cliente.telefono = telefono
        if fecha_nacimiento != '':
            cliente.fecha_nacimiento = fecha_nacimiento
        if descripcion:
            cliente.descripcion = descripcion
        cliente.save()
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
    def crear_potencial_cliente (nombre_completo, email, telefono, nacionalidad, descripcion):
        """
            Función que ingresa un nuevo potencial cliente
            Param:
                nombre_completo=nombre_completo,
                email=email,
                telefono=telefono,
                nacionalidad=nacionalidad,
                descripcion=descripcion,
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
        return aux_potencial_cliente


    @staticmethod
    def editar_potencial_cliente (potencial_cliente_id, nombre_completo=None, email=None, telefono=None, nacionalidad=None, descripcion=None):
        """
            Función modificar un potencial cliente ya ingresado en la base de datos
            Param:
                potencial_cliente_id = id del cliente a editar
                nombre_completo(Opcional)
                email(Opcional)
                telefono(Opcional)
                nacionalidad(Opcional)
                descripcion(Opcional)
            Return:
                PotencialCliente
                None en caso de NO existir el potencial cliente en la base de datos
        """
        potencial_cliente = ManagerPotencialCliente.obtener_potencial_cliente(potencial_cliente_id)
        if potencial_cliente is None:
            return None
        if nombre_completo:
            potencial_cliente.nombre_completo = nombre_completo
        if email:
            potencial_cliente.email = email
        if telefono:
            potencial_cliente.telefono = telefono
        if nacionalidad:
            potencial_cliente.nacionalidad = nacionalidad
        if descripcion:
            potencial_cliente.descripcion = descripcion
        potencial_cliente.save()
        return potencial_cliente
