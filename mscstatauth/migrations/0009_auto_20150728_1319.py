# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0008_auto_20150713_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mss',
            field=models.ManyToManyField(to='mscstatapp.Mss', verbose_name='\u0424\u0438\u043b\u0438\u0430\u043b', blank=True),
        ),
    ]
