# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mscstatapp', '0009_auto_20141208_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='sender',
            field=models.ForeignKey(related_name='sender', verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notifications',
            name='sendsms',
            field=models.BooleanField(default=False, verbose_name='\u041e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e SMS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mss',
            name='login',
            field=models.CharField(max_length=30, verbose_name='login', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mss',
            name='password',
            field=models.CharField(verbose_name='password', max_length=32, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438'),
            preserve_default=True,
        ),
    ]
