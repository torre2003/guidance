# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-06 22:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cliente', '0008_auto_20180203_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('modelo', models.CharField(choices=[('cl', 'Cliente'), ('pcl', 'PotencialCliente')], max_length=4)),
                ('modelo_id', models.PositiveIntegerField()),
                ('_info', models.TextField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nombres',
            field=models.CharField(max_length=202, verbose_name='Nombres'),
        ),
    ]
