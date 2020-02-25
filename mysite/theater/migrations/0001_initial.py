# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-25 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theaterdatado',
            fields=[
                ('t_id', models.AutoField(primary_key=True, serialize=False)),
                ('t_name', models.CharField(max_length=70)),
                ('t_area', models.CharField(max_length=20)),
                ('t_address', models.CharField(max_length=100)),
                ('t_phone', models.CharField(max_length=50)),
                ('t_webaddress', models.URLField(unique=True, verbose_name='url')),
                ('t_info', models.TextField(null=True, verbose_name='Theater Description')),
                ('t_adult', models.CharField(max_length=10)),
                ('t_kid', models.CharField(max_length=10)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('t_lat', models.CharField(max_length=30)),
                ('t_lng', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'theaterdatado',
            },
        ),
    ]
