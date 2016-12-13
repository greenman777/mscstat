# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0004_auto_20140822_0905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counter',
            options={'ordering': ['name'], 'verbose_name_plural': '\u0421\u0447\u0435\u0442\u0447\u0438\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='mss',
            options={'ordering': ['name'], 'verbose_name_plural': '\u0424\u0438\u043b\u0438\u0430\u043b\u044b'},
        ),
        migrations.AlterModelOptions(
            name='object',
            options={'ordering': ['name'], 'verbose_name_plural': '\u041e\u0431\u044a\u0435\u043a\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='typezone',
            options={'ordering': ['name'], 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0440\u0430\u0439\u043e\u043d\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['name'], 'verbose_name_plural': '\u0420\u0430\u0437\u0434\u0435\u043b\u044b'},
        ),
        migrations.AlterModelOptions(
            name='zones',
            options={'ordering': ['name'], 'verbose_name_plural': '\u0420\u0430\u0439\u043e\u043d\u044b'},
        ),
        migrations.RenameField(
            model_name='counter',
            old_name='counter_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='mss',
            old_name='mss_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='mss',
            old_name='mss_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='object',
            old_name='object_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='sites',
            old_name='site_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='sites',
            old_name='site_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='typezone',
            old_name='type_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='unit',
            old_name='unit_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='zones',
            old_name='zone_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='zones',
            old_name='zone_type',
            new_name='type',
        ),
    ]
