#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'mscstat.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'mscstat.dashboard.CustomAppIndexDashboard'
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for mscstat.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            title = 'Администрирование',
            models=('django.contrib.auth.*',
                    'mscstatauth.models.User',
                    ),
        ))

        # append an app list module for "Models"
        self.children.append(modules.Group(
            title="Справочники",
            display="tabs",
            children=[
                modules.ModelList(
                    title='Сайты',
                    models=('mscstatapp.models.Mss',)
                ),
                modules.ModelList(
                    title='Задачи',
                    models=('mscstatapp.models.Priority',
                            'mscstatapp.models.TaskStatus',)
                ),
                modules.ModelList(
                    title='Планировщик задач',
                    models=('djcelery*',),
                ),
                modules.ModelList(
                    title='SMS рассылка',
                    models=('rapidsms*',),
                ),
                modules.ModelList(
                    title='Служебные',
                    models=('mscstatapp.models.Kpi',
                            'mscstatapp.models.Subscribes',
                            'mscstatapp.models.SubscribeMessages',
                            'mscstatapp.models.Thresholds',
                            'mscstatapp.models.TkgThresholds',
                            'mscstatapp.models.CounterNoCleaning',),
                ),
            ]
        ))
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 10))
        
class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for mscstat.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
