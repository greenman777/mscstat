# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0010_auto_20141212_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438'),
            preserve_default=True,
        ),
    ]
