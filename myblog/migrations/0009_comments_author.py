# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-01 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0008_remove_comments_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.CharField(default='auth_User', max_length=20),
        ),
    ]