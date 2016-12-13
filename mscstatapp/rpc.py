#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mscstatapp.utils.extjs import RpcRouter

class ExtActionClass(object):

    def getUserData(self, user):
        return {
            'msg': {
                'id': user.id,
                'name': " ".join((user.last_name,user.first_name))}
        }
    getUserData._args_len = 0

class DirectRouter(RpcRouter):

    def __init__(self):
        self.url = 'router'
        self.actions = {
            'extAction': ExtActionClass(),
        }
        self.enable_buffer = 50