# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-30 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0025_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myblog.Categories'),
            preserve_default=False,
        ),
    ]