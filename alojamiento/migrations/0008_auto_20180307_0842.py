# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-07 08:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alojamiento', '0007_auto_20180306_1121'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ocupacionalojamiento',
            old_name='cantidad',
            new_name='huespedes',
        ),
    ]
