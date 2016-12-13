# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0016_auto_20150423_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterCleaningOld',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.ForeignKey(verbose_name='\u0441\u0447\u0435\u0442\u0447\u0438\u043a', blank=True, to='mscstatapp.Counter', null=True)),
            ],
            options={
                'ordering': ['counter'],
                'verbose_name_plural': '\u0421\u0447\u0435\u0442\u0447\u0438\u043a\u0438. \u041e\u0447\u0438\u0441\u0442\u043a\u0430 \u0438\u0441\u0442\u043e\u0440\u0438\u0438',
            },
            bases=(models.Model,),
        ),
    ]
