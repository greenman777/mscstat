# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counters',
            name='counter_name',
        ),
        migrations.RemoveField(
            model_name='counters',
            name='mss_name',
        ),
        migrations.RemoveField(
            model_name='counters',
            name='object_name',
        ),
        migrations.RemoveField(
            model_name='counters',
            name='unit_name',
        ),
    ]
