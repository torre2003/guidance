# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-03 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alojamiento', '0005_auto_20180303_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='alojamiento',
            name='habilitado',
            field=models.BooleanField(default=True),
        ),
    ]
