# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-26 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20170626_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Post',
            name='height_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='Post',
            name='width_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
