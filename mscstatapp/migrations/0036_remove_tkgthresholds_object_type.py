# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0035_auto_20150909_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tkgthresholds',
            name='object_type',
        ),
    ]
