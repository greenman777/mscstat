# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0014_auto_20150423_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='mss',
            field=models.ForeignKey(default=1, to='mscstatapp.Mss', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='type',
            field=models.ForeignKey(to='mscstatapp.ObjectType', null=True),
            preserve_default=True,
        ),
    ]
