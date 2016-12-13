# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0027_tkgmon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tkgmon',
            options={'ordering': ['kpi'], 'verbose_name_plural': '\u041f\u043e\u0440\u043e\u0433\u0438 TKG'},
        ),
    ]
