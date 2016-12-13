# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0025_auto_20150820_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': '\u0421\u043f\u0438\u0441\u043e\u043a \u043f\u043e\u0434\u043f\u0438\u0441\u043e\u043a',
            },
        ),
        migrations.AlterModelOptions(
            name='kpi',
            options={'ordering': ['name'], 'verbose_name_plural': 'KPI'},
        ),
        migrations.AlterModelOptions(
            name='subscribemessages',
            options={'ordering': ['subscribe'], 'verbose_name_plural': '\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0438 \u043d\u0430 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f'},
        ),
        migrations.RemoveField(
            model_name='subscribemessages',
            name='subscription',
        ),
        migrations.AddField(
            model_name='subscribemessages',
            name='subscribe',
            field=models.ForeignKey(verbose_name='\u041f\u043e\u0434\u043f\u0438\u0441\u043a\u0430', blank=True, to='mscstatapp.Subscribes', null=True),
        ),
    ]
