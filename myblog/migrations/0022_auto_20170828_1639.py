# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-28 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0021_auto_20170828_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]