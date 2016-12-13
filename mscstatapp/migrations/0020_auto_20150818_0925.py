# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0019_remove_object_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thresholds',
            name='night_start',
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='night_stop',
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='value_critical',
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='value_night',
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='value_normal',
        ),
    ]
