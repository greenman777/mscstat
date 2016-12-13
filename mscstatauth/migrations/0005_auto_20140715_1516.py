# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0004_remove_user_brigade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sms_notification',
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(max_length=60, verbose_name='\u0414\u043e\u043b\u0436\u043d\u043e\u0441\u0442\u044c', blank=True),
        ),
    ]
