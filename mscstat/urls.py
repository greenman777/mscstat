#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mscstatapp.views import main,reports,menu,rest,telnetstat
from mscstat import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change, password_change_done
from django.views.generic.base import RedirectView
from rapidsms.backends.kannel.views import KannelBackendView
from rest_framework.routers import DefaultRouter
import debug_toolbar
from mscstatapp.rpc import DirectRouter
from django.views.static import serve

router_direct = DirectRouter()

router = DefaultRouter(trailing_slash=False)

router.register(r'tasks', rest.TasksViewSet)
router.register(r'users', rest.UsersViewSet)
router.register(r'groups', rest.GroupsViewSet)
router.register(r'task_history', rest.TaskHistoryViewSet)
router.register(r'task_comments', rest.TaskCommentsViewSet)
router.register(r'priority', rest.PriorityViewSet)
router.register(r'mss', rest.MssViewSet)
router.register(r'object', rest.ObjectViewSet)
router.register(r'task_status', rest.TaskStatusViewSet)
router.register(r'notifications', rest.NotificationsViewSet)
router.register(r'tasks', rest.TasksViewSet)

urlpatterns = [
    url(r'^$', main.mainpage),
    url(r'^auction/', main.auction),
    url(r'^router/$', router_direct, name='router'),
    url(r'^router/api/$', router_direct.api, name='api'),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^accounts/login/$',  login,  {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', logout, {'template_name': 'logged_out.html'}),
    url(r'^accounts/change_password/$', password_change, {'template_name': 'password_change_form.html'}),
    url(r'^accounts/password_changed/$', password_change_done, {'template_name': 'password_change_done.html'}),
    url(r'^accounts/', include('rapidsms.urls.login_logout')),
    url(r'^admin/',include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^menutree/src', menu.menutree),
    url(r'^notifications_news/$', main.notifications_news),
    url(r'^send_notification/$', main.send_notification),
    url(r'^down_chart/$', main.down_chart),
    url(r'^reports/$', reports.reports),
    url(r'^export_csv/$', main.export_csv),
    url(r'^status/$', reports.status),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/media/favicon.ico', permanent=True)),

    url(r"^backend/kannel-beeline-smpp/$",KannelBackendView.as_view(backend_name="kannel-beeline-smpp")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    url(r'^', include(router.urls)),
    url (r'^__debug__/', include(debug_toolbar.urls)),
]