# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 07:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0003_remove_likeandcomment_cid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='likeandcomment',
        ),
    ]