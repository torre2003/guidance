# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from alojamiento.models import ReservaAlojamiento, OcupacionAlojamiento
from cliente.models import Cliente
from cliente.empresa.models import Empresa


class Cuenta(models.Model):
    CLIENTE = 'cl'
    EMPRESA = 'emp'
    MODELOS = (
        (CLIENTE, 'Cliente'),
        (EMPRESA, 'Empresa'),
    )
    modelo = models.CharField(
        max_length=4,
        choices=MODELOS,
    )
    modelo_id = models.PositiveIntegerField()
    saldo = models.FloatField()
    ultima_actualizacion = models.DateTimeField(null=True)

    def __unicode__(self):
        return '[{}] {}'.format(self.id, self.saldo)


class TipoTransaccionCuenta (models.Model):
    nombre = models.CharField(max_length=100, unique=True)


class TransaccionCuenta (models.Model):
    cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING)
    user = models.ForeignKey(User, models.DO_NOTHING)
    reservaalojamiento = models.ForeignKey(ReservaAlojamiento, models.DO_NOTHING, null=True)
    ocupacionalojamiento = models.ForeignKey(OcupacionAlojamiento, models.DO_NOTHING, null=True)
    tipotransaccioncuenta = models.ForeignKey(TipoTransaccionCuenta, models.DO_NOTHING)
    descripcion = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    cargo = models.FloatField(default=0)
    abono = models.FloatField(default=0)
    saldo = models.FloatField(default=0)


class TipoTransaccionCuentaPrincipal (models.Model):
    nombre = models.CharField(max_length=100, unique=True)


class TransaccionCuentaPrincipal(models.Model):
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_registro_confirmacion = models.DateTimeField(null=True)
    fecha_confirmacion = models.DateField(null=True)
    confirmada = models.BooleanField(default=True)
    tipotransaccioncuentaprincipal = models.ForeignKey(TipoTransaccionCuentaPrincipal, models.DO_NOTHING)
    transaccioncuenta = models.ForeignKey(TipoTransaccionCuenta, models.DO_NOTHING, null=True)
    descripcion = models.CharField(max_length=200, null=True)
    cargo = models.FloatField(default=0)
    abono = models.FloatField(default=0)












