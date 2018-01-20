# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-15 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='descripcion',
            field=models.CharField(default='', max_length=300, verbose_name='Descripci\xf3n'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cliente',
            name='sexo',
            field=models.CharField(default='', max_length=10, verbose_name='Sexo'),
            preserve_default=False,
        ),
    ]
