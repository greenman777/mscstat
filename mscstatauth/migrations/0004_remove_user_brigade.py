# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0003_auto_20140715_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='brigade',
        ),
    ]
