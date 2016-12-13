# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0017_countercleaningold'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CounterCleaningOld',
            new_name='CounterNoCleaning',
        ),
        migrations.AlterModelOptions(
            name='counternocleaning',
            options={'ordering': ['counter'], 'verbose_name_plural': '\u0421\u043f\u0438\u0441\u043e\u043a \u043d\u0435 \u0443\u0434\u0430\u043b\u044f\u0435\u043c\u044b\u0445 \u0441\u0447\u0435\u0442\u0447\u0438\u043a\u043e\u0432'},
        ),
    ]
