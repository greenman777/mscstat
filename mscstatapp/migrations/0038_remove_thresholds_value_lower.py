# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-05 15:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0037_auto_20160113_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thresholds',
            name='value_lower',
        ),
    ]