# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0020_auto_20150818_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='thresholds',
            name='threshold_events',
            field=models.IntegerField(null=True, verbose_name='\u0447\u0438\u0441\u043b\u043e \u0441\u043e\u0431\u044b\u0442\u0438\u0439 \u0434\u043b\u044f \u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\u043e\u0441\u0442\u0438', blank=True),
        ),
        migrations.AddField(
            model_name='thresholds',
            name='value_emergency',
            field=models.DecimalField(null=True, verbose_name='\u0430\u0432\u0430\u0440\u0438\u0439\u043d\u044b\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='thresholds',
            name='value_high',
            field=models.DecimalField(null=True, verbose_name='\u0432\u044b\u0441\u043e\u043a\u0438\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='thresholds',
            name='value_sufficient',
            field=models.DecimalField(null=True, verbose_name='\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u044b\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True),
        ),
    ]
