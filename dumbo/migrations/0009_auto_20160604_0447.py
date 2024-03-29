# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 04:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dumbo', '0008_issue_last_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, upload_to='attachment/')),
            ],
        ),
        migrations.RemoveField(
            model_name='issue',
            name='attachment',
        ),
        migrations.AddField(
            model_name='attachment',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dumbo.Issue'),
        ),
    ]
