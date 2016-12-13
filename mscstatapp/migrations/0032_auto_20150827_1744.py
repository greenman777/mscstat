# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0031_auto_20150827_1655'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='mss',
        ),
        migrations.AddField(
            model_name='objecttype',
            name='mss',
            field=models.ForeignKey(default=1, to='mscstatapp.Mss', null=True),
        ),
    ]
