# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0018_auto_20150427_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='unit',
        ),
    ]
