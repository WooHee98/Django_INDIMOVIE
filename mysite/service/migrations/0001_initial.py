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
            name='Aques',
            fields=[
                ('aq_id', models.AutoField(primary_key=True, serialize=False)),
                ('aq_title', models.CharField(max_length=50)),
                ('aq_regdate', models.DateTimeField(auto_now_add=True, verbose_name='Register Date')),
                ('aq_content', models.TextField(verbose_name='Admin-question Content')),
                ('aq_answer', models.TextField(verbose_name='Admin-question Answer')),
            ],
            options={
                'ordering': ['aq_title'],
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('faq_id', models.AutoField(primary_key=True, serialize=False)),
                ('faq_title', models.CharField(max_length=50)),
                ('faq_answer', models.TextField(verbose_name='Faq Answer')),
            ],
            options={
                'ordering': ['faq_title'],
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('n_id', models.AutoField(primary_key=True, serialize=False)),
                ('n_title', models.CharField(max_length=50)),
                ('n_regdate', models.DateTimeField(auto_now_add=True, verbose_name='Register Date')),
                ('n_content', models.TextField(verbose_name='Notice Text')),
            ],
            options={
                'ordering': ['n_title'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('se_id', models.AutoField(primary_key=True, serialize=False)),
                ('se_name', models.CharField(default=False, max_length=50)),
                ('se_description', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['se_name'],
            },
        ),
    ]
