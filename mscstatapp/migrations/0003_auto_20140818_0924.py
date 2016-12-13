# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0002_auto_20140730_1055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mss',
            options={'ordering': [b'mss_name'], 'verbose_name_plural': '\u0424\u0438\u043b\u0438\u0430\u043b\u044b'},
        ),
        migrations.AddField(
            model_name='mss',
            name='mss_title',
            field=models.CharField(default=1, max_length=30, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zones',
            name='mss',
            field=models.ForeignKey(default=1, verbose_name='\u0444\u0438\u043b\u0438\u0430\u043b', to='mscstatapp.Mss'),
            preserve_default=False,
        ),
    ]
