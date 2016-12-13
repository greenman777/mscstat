# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0007_auto_20140916_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thresholds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0440\u043e\u0433\u0430')),
                ('value_normal', models.DecimalField(verbose_name='\u043d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_digits=9, decimal_places=2)),
                ('value_night', models.DecimalField(verbose_name='\u043d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_digits=9, decimal_places=2)),
                ('value_critical', models.DecimalField(verbose_name='\u043a\u0440\u0438\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_digits=9, decimal_places=2)),
                ('night_start', models.TimeField(default=b'22:00')),
                ('night_stop', models.TimeField(default=b'06:30')),
                ('mss', models.ForeignKey(verbose_name='\u041a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440', blank=True, to='mscstatapp.Mss', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
