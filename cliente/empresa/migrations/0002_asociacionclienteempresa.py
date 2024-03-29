# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-17 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0011_auto_20180226_1125'),
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsociacionClienteEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cliente.Cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresa.Empresa')),
            ],
        ),
    ]
