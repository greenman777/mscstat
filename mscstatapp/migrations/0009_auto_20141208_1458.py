# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0008_thresholds'),
    ]

    operations = [
        migrations.AddField(
            model_name='mss',
            name='host',
            field=models.GenericIPAddressField(null=True, verbose_name='host', protocol='IPv4', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mss',
            name='login',
            field=models.CharField(default=b'login', max_length=30, verbose_name='login', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mss',
            name='password',
            field=models.CharField(default=b'password', max_length=32, verbose_name='password', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mss',
            name='port',
            field=models.IntegerField(default=6000, verbose_name='port'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thresholds',
            name='name',
            field=models.CharField(max_length=30, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0440\u043e\u0433\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='thresholds',
            name='value_normal',
            field=models.DecimalField(verbose_name='\u043d\u043e\u0440\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', max_digits=9, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
