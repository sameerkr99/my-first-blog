# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0015_auto_20170822_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='commentcount',
            field=models.IntegerField(default=0),
        ),
    ]
