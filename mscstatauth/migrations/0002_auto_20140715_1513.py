# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='organization_fax',
        ),
        migrations.RemoveField(
            model_name='user',
            name='organization_phone',
        ),
    ]
