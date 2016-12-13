# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mscstatapp', '0005_auto_20140825_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cells',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_id', models.CharField(max_length=5, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u043e\u0442\u044b', db_index=True)),
            ],
            options={
                'ordering': ['cell_id'],
                'verbose_name_plural': '\u0421\u043e\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Celltype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, verbose_name='\u0442\u0438\u043f \u0441\u043e\u0442\u044b', db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0441\u043e\u0442',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cells',
            name='celltype',
            field=models.ForeignKey(verbose_name='\u0442\u0438\u043f \u0441\u043e\u0442\u044b', to='mscstatapp.Celltype'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cells',
            name='site',
            field=models.ForeignKey(verbose_name='\u0441\u0430\u0439\u0442', to='mscstatapp.Sites'),
            preserve_default=True,
        ),
    ]
