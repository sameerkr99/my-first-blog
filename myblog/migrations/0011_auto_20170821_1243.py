# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 07:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0010_auto_20170801_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Phone',
            new_name='phone',
        ),
        migrations.AlterField(
            model_name='profile',
            name='dp',
            field=models.ImageField(default='C:/Projects/blogproject/myblog/static/profilepic/default/default_dp.png', upload_to=''),
        ),
    ]
