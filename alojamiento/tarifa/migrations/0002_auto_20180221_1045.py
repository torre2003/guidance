# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-21 10:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tarifa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temporada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('descripcion', models.CharField(max_length=300, verbose_name='Descripci\xf3n')),
            ],
        ),
        migrations.CreateModel(
            name='TemporadaFecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('temporada', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tarifa.Temporada')),
            ],
        ),
        migrations.AddField(
            model_name='tarifa',
            name='_restricciones',
            field=models.TextField(default='{}'),
        ),
    ]
