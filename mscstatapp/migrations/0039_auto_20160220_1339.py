# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-20 13:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0038_remove_thresholds_value_lower'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cells',
            name='celltype',
        ),
        migrations.RemoveField(
            model_name='cells',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sites',
            name='zone',
        ),
        migrations.RemoveField(
            model_name='zones',
            name='mss',
        ),
        migrations.RemoveField(
            model_name='zones',
            name='type',
        ),
        migrations.AlterModelOptions(
            name='commonpermissions',
            options={'permissions': (('kpi_view', 'KPI view'), ('totals_view', 'Totals view'), ('reports_all_view', 'Reports all view'), ('view_all_tasks', 'View all tasks'))},
        ),
        migrations.DeleteModel(
            name='Cells',
        ),
        migrations.DeleteModel(
            name='Celltype',
        ),
        migrations.DeleteModel(
            name='Sites',
        ),
        migrations.DeleteModel(
            name='Typezone',
        ),
        migrations.DeleteModel(
            name='Zones',
        ),
    ]
