# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cliente.models import Cliente


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


def obtener_clientes():
    """
        Función que los clientes ingresados en el sistema
        Param:
        Return:
            ResultSet<Cliente>
            
    """
    clientes = Cliente.objects.all()
    return clientes


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
    if obtener_cliente_por_rut(rut) is not None:
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

def editar_cliente (cliente_id, rut=None, digito_verificador=None, nombres=None, apellidos=None, direccion=None, ciudad=None, pais=None, email=None, sexo=None, telefono=None, fecha_nacimiento = None, descripcion=None):
    """
        Función 
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
            None en caso de existir el cliente en la base de datos
    """
    cliente = obtener_cliente(cliente_id)
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
    if fecha_nacimiento:
        cliente.fecha_nacimiento = fecha_nacimiento
    if descripcion:
        cliente.descripcion = descripcion
    cliente.save()
    return cliente



