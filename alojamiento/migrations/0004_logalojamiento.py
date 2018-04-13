# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-01 08:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alojamiento', '0003_auto_20180226_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogAlojamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modelo', models.CharField(choices=[('cv', 'CanalVenta'), ('ta', 'TipoAlojamiento'), ('a', 'Alojamiento'), ('ra', 'ReservaAlojamiento'), ('oa', 'OcupacionAlojamiento')], max_length=4)),
                ('modelo_id', models.PositiveIntegerField()),
                ('_info', models.TextField(default='{}')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]