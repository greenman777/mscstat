# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatauth', '0006_auto_20140822_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sms_notification',
            field=models.BooleanField(default=True, verbose_name='\u0421\u041c\u0421 \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u0435'),
            preserve_default=True,
        ),
    ]
