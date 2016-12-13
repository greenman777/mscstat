# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 14:29
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0039_auto_20160220_1339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='counters',
            options={'ordering': ['datetime_start'], 'verbose_name_plural': 'Статистика'},
        ),
        migrations.AlterModelOptions(
            name='notifications',
            options={'ordering': ['date'], 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.AlterModelOptions(
            name='priority',
            options={'ordering': ['name'], 'verbose_name_plural': 'Пиоритет задачи'},
        ),
        migrations.AlterModelOptions(
            name='taskcomments',
            options={'ordering': ['pk'], 'verbose_name_plural': 'Комментарии к задаче'},
        ),
        migrations.AlterModelOptions(
            name='taskhistory',
            options={'ordering': ['pk'], 'verbose_name_plural': 'История задачи'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'ordering': ['create_date'], 'verbose_name_plural': 'Задачи'},
        ),
        migrations.AlterModelOptions(
            name='taskstatus',
            options={'ordering': ['name'], 'verbose_name_plural': 'Статус задачи'},
        ),
        migrations.AlterField(
            model_name='tkgthresholds',
            name='object_name',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='mss', chained_model_field='mss', null=True, on_delete=django.db.models.deletion.CASCADE, to='mscstatapp.Object', verbose_name='Объект мониторинга'),
        ),
    ]
