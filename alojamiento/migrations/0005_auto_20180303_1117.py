# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-03 11:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alojamiento', '0004_logalojamiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alojamiento',
            name='capacidad',
        ),
        migrations.AddField(
            model_name='tipoalojamiento',
            name='capacidad',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
