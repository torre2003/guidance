# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-17 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_auto_20180116_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_nacimiento',
            field=models.DateField(null=True),
        ),
    ]
