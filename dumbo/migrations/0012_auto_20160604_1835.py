# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dumbo', '0011_project_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_picture/', verbose_name='Profile Picture'),
        ),
    ]