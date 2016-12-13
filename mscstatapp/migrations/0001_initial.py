# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter_name', models.CharField(max_length=100, db_index=True)),
            ],
            options={
                'ordering': [b'counter_name'],
                'verbose_name_plural': '\u0421\u0447\u0435\u0442\u0447\u0438\u043a\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Counters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mss_name', models.CharField(max_length=30, db_index=True)),
                ('unit_name', models.CharField(max_length=60, db_index=True)),
                ('object_name', models.CharField(max_length=60, db_index=True)),
                ('counter_name', models.CharField(max_length=100, db_index=True)),
                ('counter_value', models.DecimalField(max_digits=9, decimal_places=2)),
                ('datetime_start', models.DateTimeField(db_index=True)),
                ('counter', models.ForeignKey(verbose_name='\u0441\u0447\u0435\u0442\u0447\u0438\u043a', blank=True, to='mscstatapp.Counter', null=True)),
            ],
            options={
                'ordering': [b'datetime_start'],
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mss_name', models.CharField(max_length=30, db_index=True)),
            ],
            options={
                'ordering': [b'mss_name'],
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='counters',
            name='mss',
            field=models.ForeignKey(verbose_name='\u043a\u043e\u043c\u043c\u0443\u0442\u0430\u0442\u043e\u0440', blank=True, to='mscstatapp.Mss', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u043e\u043f\u0435\u0440\u0430\u0446\u0438\u0438')),
                ('message', models.CharField(max_length=150, verbose_name='\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435')),
                ('read', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u043e')),
                ('user', models.ForeignKey(verbose_name='\u041f\u043e\u043b\u0443\u0447\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'date'],
                'verbose_name_plural': '\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_name', models.CharField(max_length=60, db_index=True)),
            ],
            options={
                'ordering': [b'object_name'],
                'verbose_name_plural': '\u041e\u0431\u044a\u0435\u043a\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='counters',
            name='object',
            field=models.ForeignKey(verbose_name='\u043e\u0431\u044a\u0435\u043a\u0442', blank=True, to='mscstatapp.Object', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442')),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name_plural': '\u041f\u0438\u043e\u0440\u0438\u0442\u0435\u0442 \u0437\u0430\u0434\u0430\u0447\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_name', models.CharField(max_length=30, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0430\u0439\u0442\u0430', db_index=True)),
                ('site_2g', models.BooleanField(default=True, verbose_name='\u0441\u0430\u0439\u0442 2G')),
                ('site_3g', models.BooleanField(default=False, verbose_name='\u0441\u0430\u0439\u0442 3G')),
                ('site_id', models.CharField(max_length=5, verbose_name='\u043d\u043e\u043c\u0435\u0440 \u0441\u0430\u0439\u0442\u0430', db_index=True)),
                ('site_address', models.CharField(max_length=60, verbose_name='\u0430\u0434\u0440\u0435\u0441', db_index=True)),
            ],
            options={
                'ordering': [b'site_id'],
                'verbose_name_plural': '\u0421\u0430\u0439\u0442\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=100, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
                ('create_date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'pk'],
                'verbose_name_plural': '\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0438 \u043a \u0437\u0430\u0434\u0430\u0447\u0435',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=100, verbose_name='\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439')),
                ('create_date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('corrector', models.ForeignKey(verbose_name='\u041a\u043e\u0440\u0440\u0435\u043a\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [b'pk'],
                'verbose_name_plural': '\u0418\u0441\u0442\u043e\u0440\u0438\u044f \u0437\u0430\u0434\u0430\u0447\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=80, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('description', models.CharField(max_length=160, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('create_date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f')),
                ('execution_date', models.DateField(verbose_name='\u0414\u0430\u0442\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f')),
                ('author', models.ForeignKey(verbose_name='\u0410\u0432\u0442\u043e\u0440', to=settings.AUTH_USER_MODEL)),
                ('performer', models.ForeignKey(verbose_name='\u0418\u0441\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL)),
                ('priority', models.ForeignKey(verbose_name='\u041f\u0440\u0438\u043e\u0440\u0438\u0442\u0435\u0442', to='mscstatapp.Priority')),
            ],
            options={
                'ordering': [b'create_date'],
                'verbose_name_plural': '\u0417\u0430\u0434\u0430\u0447\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taskhistory',
            name='task',
            field=models.ForeignKey(verbose_name='\u0417\u0430\u0434\u0430\u0447\u0430', to='mscstatapp.Tasks'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskcomments',
            name='task',
            field=models.ForeignKey(verbose_name='\u0417\u0430\u0434\u0430\u0447\u0430', to='mscstatapp.Tasks'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438')),
            ],
            options={
                'ordering': [b'name'],
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0443\u0441 \u0437\u0430\u0434\u0430\u0447\u0438',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tasks',
            name='status',
            field=models.ForeignKey(verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', to='mscstatapp.TaskStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskhistory',
            name='status',
            field=models.ForeignKey(verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', to='mscstatapp.TaskStatus'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Typezone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type_name', models.CharField(max_length=30, verbose_name='\u0442\u0438\u043f \u0440\u0430\u0439\u043e\u043d\u0430', db_index=True)),
            ],
            options={
                'ordering': [b'type_name'],
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0440\u0430\u0439\u043e\u043d\u043e\u0432',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_name', models.CharField(max_length=60, db_index=True)),
            ],
            options={
                'ordering': [b'unit_name'],
                'verbose_name_plural': '\u0420\u0430\u0437\u0434\u0435\u043b\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='counters',
            name='unit',
            field=models.ForeignKey(verbose_name='\u0440\u0430\u0437\u0434\u0435\u043b', blank=True, to='mscstatapp.Unit', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Zones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('zone_name', models.CharField(max_length=30, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0440\u0430\u0439\u043e\u043d\u0430', db_index=True)),
                ('population', models.IntegerField(verbose_name='\u043d\u0430\u0441\u0435\u043b\u0435\u043d\u0438\u0435')),
                ('zone_type', models.ForeignKey(verbose_name='\u0442\u0438\u043f \u0440\u0430\u0439\u043e\u043d\u0430', to='mscstatapp.Typezone')),
            ],
            options={
                'ordering': [b'zone_name'],
                'verbose_name_plural': '\u0420\u0430\u0439\u043e\u043d\u044b',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sites',
            name='zone',
            field=models.ForeignKey(verbose_name='\u0440\u0430\u0439\u043e\u043d', to='mscstatapp.Zones'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='CommonPermissions',
            fields=[
            ],
            options={
                'proxy': True,
                'permissions': ((b'kpi_view', b'KPI view'), (b'region_view', b'Region view'), (b'sites_view', b'Sites view'), (b'totals_view', b'Totals view'), (b'profit_view', b'Profit view'), (b'reports_all_view', b'Reports all view'), (b'view_all_tasks', b'View all tasks')),
            },
            bases=('mscstatapp.mss',),
        ),
    ]
