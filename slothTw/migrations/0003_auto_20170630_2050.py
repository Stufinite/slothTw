# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 12:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slothTw', '0002_auto_20170616_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
