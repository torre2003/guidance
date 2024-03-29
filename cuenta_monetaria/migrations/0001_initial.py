# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-15 21:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alojamiento', '0009_auto_20180408_1247'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(choices=[('cl', 'Cliente'), ('emp', 'Empresa')], max_length=4)),
                ('modelo_id', models.PositiveIntegerField()),
                ('saldo', models.FloatField()),
                ('ultima_actualizacion', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoTransaccionCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoTransaccionCuentaPrincipal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransaccionCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cargo', models.FloatField(default=0)),
                ('abono', models.FloatField(default=0)),
                ('saldo', models.FloatField(default=0)),
                ('cuenta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cuenta_monetaria.Cuenta')),
                ('ocupacionalojamiento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.OcupacionAlojamiento')),
                ('reservaalojamiento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='alojamiento.ReservaAlojamiento')),
                ('tipotransaccioncuenta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cuenta_monetaria.TipoTransaccionCuenta')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransaccionCuentaPrincipal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_registro_confirmacion', models.DateTimeField(null=True)),
                ('fecha_confirmacion', models.DateField(null=True)),
                ('confirmada', models.BooleanField(default=True)),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('cargo', models.FloatField(default=0)),
                ('abono', models.FloatField(default=0)),
                ('tipotransaccioncuentaprincipal', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cuenta_monetaria.TipoTransaccionCuentaPrincipal')),
                ('transaccioncuenta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cuenta_monetaria.TipoTransaccionCuenta')),
            ],
        ),
    ]
