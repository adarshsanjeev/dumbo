# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-03 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dumbo', '0007_auto_20160603_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='last_updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]