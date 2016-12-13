# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0028_auto_20150824_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='TkgThresholds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value_high', models.DecimalField(null=True, verbose_name='\u0432\u044b\u0441\u043e\u043a\u0438\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True)),
                ('value_sufficient', models.DecimalField(null=True, verbose_name='\u0434\u043e\u0441\u0442\u0430\u0442\u043e\u0447\u043d\u044b\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True)),
                ('value_emergency', models.DecimalField(null=True, verbose_name='\u0430\u0432\u0430\u0440\u0438\u0439\u043d\u044b\u0439 \u043f\u043e\u0440\u043e\u0433', max_digits=9, decimal_places=2, blank=True)),
                ('threshold_events', models.IntegerField(null=True, verbose_name='\u0447\u0438\u0441\u043b\u043e \u0441\u043e\u0431\u044b\u0442\u0438\u0439 \u0434\u043b\u044f \u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u043d\u043e\u0441\u0442\u0438', blank=True)),
                ('threshold_active', models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439')),
                ('kpi', models.ForeignKey(verbose_name='KPI', blank=True, to='mscstatapp.Kpi', null=True)),
                ('mss', models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440', blank=True, to='mscstatapp.Mss', null=True)),
                ('object_name', models.ForeignKey(verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', blank=True, to='mscstatapp.Object', null=True)),
                ('object_type', models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043e\u0431\u044a\u0435\u043a\u0442\u0430', blank=True, to='mscstatapp.ObjectType', null=True)),
            ],
            options={
                'ordering': ['kpi'],
                'verbose_name_plural': '\u041f\u043e\u0440\u043e\u0433\u0438 TKG',
            },
        ),
        migrations.RemoveField(
            model_name='tkgmon',
            name='kpi',
        ),
        migrations.RemoveField(
            model_name='tkgmon',
            name='mss',
        ),
        migrations.RemoveField(
            model_name='tkgmon',
            name='object_name',
        ),
        migrations.RemoveField(
            model_name='tkgmon',
            name='object_type',
        ),
        migrations.DeleteModel(
            name='TkgMon',
        ),
    ]
