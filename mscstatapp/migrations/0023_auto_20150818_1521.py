# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0022_auto_20150818_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribemessages',
            options={'ordering': ['subscription'], 'verbose_name_plural': '\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0438 \u043d\u0430 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f'},
        ),
        migrations.AlterModelOptions(
            name='thresholds',
            options={'ordering': ['name'], 'verbose_name_plural': '\u041f\u043e\u0440\u043e\u0433\u0438 KPI'},
        ),
    ]
