# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-21 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0009_auto_20180206_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='_info',
            field=models.TextField(default='{}'),
        ),
    ]
