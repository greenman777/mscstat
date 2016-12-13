# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0015_auto_20150423_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='unit',
            field=models.ForeignKey(to='mscstatapp.Unit', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mss',
            name='port',
            field=models.IntegerField(default=6000, verbose_name='port', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mss',
            name='title',
            field=models.CharField(db_index=True, max_length=30, verbose_name='\u0444\u0438\u043b\u0438\u0430\u043b', blank=True),
            preserve_default=True,
        ),
    ]
