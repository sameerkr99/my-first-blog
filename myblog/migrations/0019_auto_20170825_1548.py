# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-25 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0018_auto_20170824_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(blank=True, upload_to='/profilepic/'),
        ),
    ]