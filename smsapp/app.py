#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rapidsms.apps.base import AppBase

class SmsApp (AppBase):
    
    def handle(self, msg):
        if msg.text == 'ping':
            msg.respond('pongDIMON')
            print("!!!!!!!!!!!!")
            return True
        return False