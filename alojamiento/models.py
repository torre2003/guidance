# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from cliente.models import Cliente
from cliente.empresa.models import Empresa
from alojamiento.tarifa.models import Tarifa
from django.contrib.auth.models import User


class CanalVenta (models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')
    habilitado = models.BooleanField(default=True)


class TipoAlojamiento (models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')
    habilitado = models.BooleanField(default=True)
    capacidad = models.PositiveIntegerField()


class Alojamiento (models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codigo = models.CharField(max_length=15, verbose_name='Código')
    tipoalojamiento = models.ForeignKey(TipoAlojamiento, models.DO_NOTHING)
    habilitado = models.BooleanField(default=True)


class Comentario(models.Model):
    texto = models.CharField(max_length=50)


class ReservaAlojamiento (models.Model):
    CONFIRMANDO_PAGO = 'confirmando_pago'
    PAGADA = 'pagada'
    CONFIRMADA = 'confirmada'
    CANCELADA = 'cancelada'
    ESTADOS = (
        (CONFIRMANDO_PAGO, 'Confirmando pago'),
        (PAGADA, 'Pagada'),
        (CONFIRMADA, 'Confirmada'),
        (CANCELADA, 'Cancelada'),
    )
    estado = models.CharField(max_length=30,choices=ESTADOS)
    fecha_reservacion = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    empresa = models.ForeignKey(Empresa, models.DO_NOTHING, null=True)
    # canalventa = models.ForeignKey(CanalVenta, models.DO_NOTHING)
    _comentario = models.TextField(default='{}')

    def get_comentario(self):
        return json.loads(self._comentario)

    def set_comentario(self, value):
        self._comentario = json.dumps(value, ensure_ascii=False)

    comentario = property(get_comentario, set_comentario)

    @staticmethod
    def isEstado (estado):
        estados = [item for item in ReservaAlojamiento.ESTADOS if item[0] == estado]
        if len(estados) > 0:
            return True
        return False


class OcupacionAlojamiento(models.Model):
    alojamiento = models.ForeignKey(Alojamiento, models.DO_NOTHING)
    reservaalojamiento = models.ForeignKey(ReservaAlojamiento, models.DO_NOTHING)
    huespedes = models.IntegerField()
    fecha = models.DateField()
    canalventa = models.ForeignKey(CanalVenta, models.DO_NOTHING)
    tarifa = models.ForeignKey(Tarifa, models.DO_NOTHING)
    valor = models.FloatField()
    cautiva = models.BooleanField(default=True)


class LogAlojamiento(models.Model):
    CANALVENTA = 'cv'
    TIPOALOJAMIENTO = 'ta'
    ALOJAMIENTO = 'a'
    RESERVAALOJAMIENTO = 'ra'
    OCUPACIONALOJAMIENTO = 'oa'
    MODELOS = (
        (CANALVENTA, 'CanalVenta'),
        (TIPOALOJAMIENTO, 'TipoAlojamiento'),
        (ALOJAMIENTO, 'Alojamiento'),
        (RESERVAALOJAMIENTO, 'ReservaAlojamiento'),
        (OCUPACIONALOJAMIENTO, 'OcupacionAlojamiento'),
    )
    fecha = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    modelo = models.CharField(
        max_length=4,
        choices=MODELOS,
    )
    modelo_id = models.PositiveIntegerField()
    _info = models.TextField(default='{}')

    def get_info(self):
        return json.loads(self._info)

    def set_info(self, value):
        self._info = json.dumps(value, ensure_ascii=False)

    info = property(get_info, set_info)