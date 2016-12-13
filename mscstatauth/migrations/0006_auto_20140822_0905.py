# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0004_auto_20140822_0905'),
        ('mscstatauth', '0005_auto_20140715_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mss',
            field=models.ManyToManyField(to='mscstatapp.Mss', null=True, verbose_name='\u0424\u0438\u043b\u0438\u0430\u043b', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
