# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from cliente.models import Cliente

class Empresa (models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    rut = models.CharField(max_length=20, verbose_name='Rut')
    digito_verificador = models.CharField(max_length=1, verbose_name='Dígito verificador')
    telefono = models.CharField(max_length=100, verbose_name='Télefono')
    direccion = models.CharField(max_length=300, verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')


class AsociacionClienteEmpresa(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING)
    fecha_creacion = models.DateField(auto_now_add=True)