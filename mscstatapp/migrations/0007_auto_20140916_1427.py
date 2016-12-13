# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0006_auto_20140904_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cells',
            name='cell_id',
            field=models.CharField(unique=True, max_length=5, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u043e\u0442\u044b', db_index=True),
        ),
        migrations.AlterField(
            model_name='sites',
            name='site_id',
            field=models.CharField(unique=True, max_length=5, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u0430\u0439\u0442\u0430', db_index=True),
        ),
    ]
