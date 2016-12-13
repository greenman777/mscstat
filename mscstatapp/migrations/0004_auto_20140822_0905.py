# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0003_auto_20140818_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mss',
            name='mss_name',
            field=models.CharField(max_length=30, verbose_name='\u043a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440', db_index=True),
        ),
        migrations.AlterField(
            model_name='mss',
            name='mss_title',
            field=models.CharField(max_length=30, verbose_name='\u0444\u0438\u043b\u0438\u0430\u043b', db_index=True),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(related_name=b'user', verbose_name='\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='status',
            field=models.ForeignKey(related_name=b'status', verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', to='mscstatapp.TaskStatus'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='author',
            field=models.ForeignKey(related_name=b'author', verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='performer',
            field=models.ForeignKey(related_name=b'performer', verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
    ]
