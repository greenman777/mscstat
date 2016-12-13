# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0024_thresholds_higher_better'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kpi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 KPI', blank=True)),
                ('higher_better', models.BooleanField(default=True, verbose_name='\u0432\u044b\u0448\u0435 \u043b\u0443\u0447\u0448\u0435')),
            ],
        ),
        migrations.AlterModelOptions(
            name='thresholds',
            options={'ordering': ['kpi'], 'verbose_name_plural': '\u041f\u043e\u0440\u043e\u0433\u0438 KPI'},
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='higher_better',
        ),
        migrations.RemoveField(
            model_name='thresholds',
            name='name',
        ),
        migrations.AddField(
            model_name='thresholds',
            name='kpi',
            field=models.ForeignKey(verbose_name='KPI', blank=True, to='mscstatapp.Kpi', null=True),
        ),
    ]
