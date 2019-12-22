# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.db import models
from django.contrib.auth.models import User



class Temporada(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')


class TemporadaFecha(models.Model):
    fecha = models.DateField()
    temporada = models.ForeignKey(Temporada, models.DO_NOTHING)

    class Meta:
        unique_together = (
            ("fecha",),
        )


class Tarifa(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')
    habilitado = models.BooleanField(default=True)

    _restricciones = models.TextField(default='{}')
    def get_restricciones(self):
        return json.loads(self._restricciones)
    def set_restricciones(self, value):
        self._restricciones = json.dumps(value, ensure_ascii=False)
    restricciones = property(get_restricciones, set_restricciones)

    _valores = models.TextField(default='{}')
    def get_valores(self):
        return json.loads(self._valores)
    def set_valores(self, value):
        self._valores = json.dumps(value, ensure_ascii=False)
    valores = property(get_valores, set_valores)


class LogTarifa(models.Model):
    TEMPORADA = 'te'
    TEMPORADA_FECHA = 'tf'
    TARIFA = 'ta'
    
    MODELOS = (
        (TEMPORADA, 'Temporada'),
        (TEMPORADA_FECHA, 'TemporadaFecha'),
        (TARIFA, 'Tarifa'),
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