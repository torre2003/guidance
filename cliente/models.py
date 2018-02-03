# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Cliente(models.Model):
    nombres = models.CharField(max_length=200, verbose_name='Nombres')
    apellidos = models.CharField(max_length=200, verbose_name='Apellidos')
    direccion = models.CharField(max_length=300, verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    pais = models.CharField(max_length=100, verbose_name='País')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    sexo = models.CharField(max_length=10, verbose_name='Sexo')
    telefono = models.CharField(max_length=100, verbose_name='Télefono')
    rut = models.CharField(max_length=20, verbose_name='Rut')
    digito_verificador = models.CharField(max_length=1, verbose_name='Dígito verificador')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')
    fecha_nacimiento = models.DateField(null=True)


class PotencialCliente(models.Model):
    nombre_completo = models.CharField(max_length=300, verbose_name='Nombre Completo')
    email = models.CharField(max_length=100, verbose_name='E-mail', null=True)
    telefono = models.CharField(max_length=100, verbose_name='Teléfono', null=True)
    nacionalidad = models.CharField(max_length=100, verbose_name='Nacionalidad')
    descripcion = models.CharField(max_length=500, verbose_name='Descripción', null=True)
    fecha = models.DateField(auto_now_add=True)