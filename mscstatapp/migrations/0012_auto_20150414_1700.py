# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0011_auto_20141212_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='zones',
            options={'ordering': ['mss', 'name'], 'verbose_name_plural': '\u0420\u0430\u0439\u043e\u043d\u044b'},
        ),
        migrations.AlterField(
            model_name='sites',
            name='address',
            field=models.CharField(max_length=120, verbose_name='\u0430\u0434\u0440\u0435\u0441', db_index=True),
            preserve_default=True,
        ),
    ]
