# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mscstatapp', '0021_auto_20150818_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeMessages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscription', models.CharField(max_length=30, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0438', blank=True)),
                ('subscribe_active', models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u043d\u0430\u044f')),
                ('mss', models.ForeignKey(verbose_name='\u0424\u0438\u043b\u0438\u0430\u043b', blank=True, to='mscstatapp.Mss', null=True)),
                ('recipient', models.ForeignKey(related_name='recipient', verbose_name='\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='thresholds',
            name='threshold_active',
            field=models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439'),
        ),
    ]
