# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-03 13:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarifa', '0003_auto_20180226_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarifa',
            name='valor',
        ),
    ]
