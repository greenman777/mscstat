# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0002_auto_20140715_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_short',
            field=models.CharField(max_length=5, verbose_name='\u041a\u043e\u0440\u043e\u0442\u043a\u0438\u0439 \u043d\u043e\u043c\u0435\u0440', blank=True),
        ),
    ]
