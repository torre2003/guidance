# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-21 10:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tarifa', '0001_initial'),
        ('cliente', '0010_auto_20180221_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alojamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('codigo', models.CharField(max_length=15, verbose_name='C\xf3digo')),
                ('capacidad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CanalVenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=300, verbose_name='Descripci\xf3n')),
                ('habilitado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OcupacionAlojamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('_info', models.TextField(default='{}')),
                ('valor', models.FloatField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.Alojamiento')),
                ('canalventa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.CanalVenta')),
                ('tarifa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tarifa.Tarifa')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaAlojamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('confirmando_pago', 'Confirmando pago'), ('pagada', 'Pagada'), ('comfirmada', 'Comfirmada'), ('cancelada', 'Cancelada')], max_length=30)),
                ('fecha_reservacion', models.DateTimeField(auto_now_add=True)),
                ('canalventa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.CanalVenta')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cliente', to='cliente.Cliente')),
                ('cliente_secundario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cliente_secundario', to='cliente.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='TipoAlojamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=300, verbose_name='Descripci\xf3n')),
                ('habilitado', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='alojamiento',
            name='tipoalojamiento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.TipoAlojamiento'),
        ),
    ]
