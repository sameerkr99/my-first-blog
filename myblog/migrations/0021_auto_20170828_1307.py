# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-28 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0020_auto_20170828_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='dp',
            field=models.CharField(default='/profilepic/default/default_dp.png', max_length=1000),
        ),
    ]
