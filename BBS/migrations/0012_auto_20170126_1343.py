# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-26 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BBS', '0011_auto_20170124_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bbs_title',
            name='name',
            field=models.CharField(max_length=50, verbose_name='xingming'),
        ),
    ]