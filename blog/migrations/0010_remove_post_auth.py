# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-04 10:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170204_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='auth',
        ),
    ]
