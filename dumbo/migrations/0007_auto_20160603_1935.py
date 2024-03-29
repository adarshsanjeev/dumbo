# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-03 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dumbo', '0006_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('UNCONFIRMED', 'UNCONFIRMED'), ('CONFIRMED', 'CONFIRMED'), ('PATCH', 'PATCH'), ('CLOSED', 'CLOSED')], default='UNCONFIRMED', max_length=11, verbose_name='Add a tag to the issue'),
        ),
    ]
