# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cliente.models import Cliente





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


def obtener_cliente_por_rut (rut):
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
