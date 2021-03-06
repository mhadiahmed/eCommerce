# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-06 15:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('blog', '0004_auto_20170105_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='post',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='auth',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
