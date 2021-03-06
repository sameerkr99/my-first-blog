# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-21 08:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_auto_20170821_1243'),
    ]

    operations = [
        migrations.CreateModel(
            name='upvotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('upvote', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.Post')),
            ],
        ),
    ]
