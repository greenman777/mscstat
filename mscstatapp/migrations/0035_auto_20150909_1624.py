# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0034_auto_20150908_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objecttype',
            name='object',
            field=models.ForeignKey(to='mscstatapp.Object', null=True),
        ),
        migrations.AlterField(
            model_name='tkgthresholds',
            name='object_type',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'object', chained_field=b'object_name', verbose_name='\u0422\u0438\u043f \u043e\u0431\u044a\u0435\u043a\u0442\u0430', blank=True, auto_choose=True, to='mscstatapp.ObjectType', null=True),
        ),
    ]
