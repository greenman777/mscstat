# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0029_auto_20150824_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tkgthresholds',
            name='object_name',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'object_type', chained_field=b'object_type', verbose_name='\u041e\u0431\u044a\u0435\u043a\u0442 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430', blank=True, auto_choose=True, to='mscstatapp.Object', null=True),
        ),
    ]
