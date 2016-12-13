# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0013_auto_20150423_1329'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60, db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': '\u0422\u0438\u043f \u043e\u0431\u044a\u0435\u043a\u0442\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='object',
            name='mss',
        ),
        migrations.RemoveField(
            model_name='object',
            name='type',
        ),
    ]
