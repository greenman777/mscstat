# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0012_auto_20150414_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='mss',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440', to='mscstatapp.Mss', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='type',
            field=models.CharField(db_index=True, max_length=60, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thresholds',
            name='value_night',
            field=models.DecimalField(verbose_name='\u043d\u043e\u0447\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
    ]
