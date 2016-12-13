# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0023_auto_20150818_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='thresholds',
            name='higher_better',
            field=models.BooleanField(default=True, verbose_name='\u0432\u044b\u0448\u0435 \u043b\u0443\u0447\u0448\u0435'),
        ),
    ]
