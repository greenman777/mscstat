# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0033_auto_20150828_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='type',
        ),
        migrations.RemoveField(
            model_name='objecttype',
            name='mss',
        ),
        migrations.AddField(
            model_name='object',
            name='mss',
            field=models.ForeignKey(default=1, to='mscstatapp.Mss', null=True),
        ),
        migrations.AddField(
            model_name='objecttype',
            name='object',
            field=models.ForeignKey(default=1, to='mscstatapp.Object', null=True),
        ),
        migrations.AlterField(
            model_name='tkgthresholds',
            name='object_name',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'mss', chained_field=b'mss', verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', blank=True, auto_choose=True, to='mscstatapp.Object', null=True),
        ),
        migrations.AlterField(
            model_name='tkgthresholds',
            name='object_type',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'object', chained_field=b'object', verbose_name='\u0422\u0438\u043f \u043e\u0431\u044a\u0435\u043a\u0442\u0430', blank=True, auto_choose=True, to='mscstatapp.ObjectType', null=True),
        ),
    ]
