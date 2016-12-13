#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from celery.task import task

from mscstatapp.views.telnetstat import telnet_exec,reply_parser
from mscstatapp.views import reports
from mscstatapp import models
from datetime import datetime, timedelta
import re
from rapidsms.router import send, lookup_connections
from django.core import cache as cache_module
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

from mscstatapp.utils.snmp_service import cbFun
from twisted.internet import reactor
from pysnmp.entity import engine, config
from pysnmp.carrier.twisted import dispatch
from pysnmp.carrier.twisted.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.carrier.error import CarrierError

@task(ignore_result=True)
def statistic_clear():
    models.Counters.objects.filter(datetime_start__lt = (datetime.now() - timedelta(days=30))).exclude(counter__in=models.CounterNoCleaning.objects.values_list('counter')).delete()

@task(ignore_result=True)
def message_alarm_kpi(mss_name):
    mss = models.Mss.objects.get(name=mss_name)
    status = reports.status(mss=mss)
    if status['flag_alarm']:
        kpi = status['content'][0]
        message = " ".join((kpi['filial'],kpi['date'],kpi['time'],"CSetR:",kpi['csetr'],"SucV:",kpi['sucv'],"mACR:",kpi['macr'],"Calls:",kpi['calls'],"IN abort:",kpi['in_abort']))
        message = re.sub(r'\<[^>]*\>', '', message)
        subscribes = models.SubscribeMessages.objects.filter(mss=mss,subscribe__name='Alarm KPI',subscribe_active=True)
        for subscribe in subscribes:
            if (subscribe.recipient.sms_notification and (len(subscribe.recipient.phone)==11)):
                phone = "".join(("7",subscribe.recipient.phone[1:]))
                connections = lookup_connections(backend="kannel-beeline-smpp",identities=[phone])
                send(message, connections=connections)

@task(ignore_result=True)
def statistic_save(uuid,mss_name):
    kpi_cache = cache_module.caches['default']
    kpi_list = kpi_cache.get(uuid)
    try:
        for kpi in kpi_list:
            unit, created = models.Unit.objects.get_or_create(name=kpi["unit_name"])
            counter, created = models.Counter.objects.get_or_create(name=kpi["counter_name"])
            mss, created = models.Mss.objects.get_or_create(name=kpi["mss_name"])
            object, create = models.Object.objects.get_or_create(name=kpi["object_name"],mss=mss)
            type, create = models.ObjectType.objects.get_or_create(name=kpi["object_type"],object=object)
            if not create:
                object.type = type
                object.save()
            try:
                counters, create = models.Counters.objects.get_or_create(mss=mss,unit=unit,object=object,counter=counter,datetime_start=kpi["datetime_start"],defaults={'counter_value': kpi["counter_value"]})
            except ObjectDoesNotExist:
                print("Doesn't exist.",{'mss':mss,'unit':unit,'object':object,'object_type':kpi["object_type"],'counter':counter,'datetime_start':kpi["datetime_start"],'counter_value':kpi["counter_value"]})
            except MultipleObjectsReturned:
                print("MultipleObjects",{'mss':mss,'unit':unit,'object':object,'object_type':kpi["object_type"],'counter':counter,'datetime_start':kpi["datetime_start"],'counter_value':kpi["counter_value"]})
            except UnboundLocalError:
                print("UnboundLocalError",{'mss':mss,'unit':unit,'object':object,'object_type':kpi["object_type"],'counter':counter,'datetime_start':kpi["datetime_start"],'counter_value':kpi["counter_value"]})
            if not create:
                counters.counter_value = kpi["counter_value"]
                counters.save()
        message_alarm_kpi.delay(mss.name)
    except TypeError:
        print(mss_name,"kpi_list: ",kpi_list,' TypeError')

@task(ignore_result=True)
def statistic_load():
    for mss in models.Mss.objects.all():
        tasks = []
        kpi_list = []
        status,results = telnet_exec(host=mss.host,port=mss.port,login=mss.login,password=mss.get_crypto(),buffer='LST TRFINF: STATE=ACT,TO=TNAME;' + "\n")
        if status == "Logged successfully":
            for result in results:
                task_find = reply_parser(result)
                if task_find:
                    tasks += task_find
            for task in tasks:
                status, results = telnet_exec(host=mss.host,port=mss.port,login=mss.login,password=mss.get_crypto(),buffer='LST TRFRPT:TSKNAME="'+task+'", ENTTYPE=ORG, RPTTYPE=NML;' + "\n")
                if status == "Logged successfully":
                    for result in results:
                        kpi = reply_parser(result)
                        kpi_list += kpi
        if len(kpi_list):
            kpi_cache = cache_module.caches['default']
            uuid = ""
            kpi_cache.set(uuid, kpi_list[:])
            statistic_save.delay(uuid, mss.name)

# Run Twisted main loop
@task(bind=True,ignore_result=True)
def snmp_trap_receiver(self):
    try:
        # Create SNMP engine with autogenernated engineID and pre-bound
        # to socket transport dispatcher
        snmpEngine = engine.SnmpEngine()
        # Transport setup
        # UDP over IPv4
        snmpEngine.registerTransportDispatcher(dispatch.TwistedDispatcher())
        config.addSocketTransport(snmpEngine, udp.domainName, udp.UdpTwistedTransport().openServerMode(('127.0.0.1', 1162)))
        # SNMPv1 setup (Manager role)
        # SecurityName <-> CommunityName <-> Transport mapping
        config.addV1System(snmpEngine, 'krv_emerson_1', 'public')
        config.addV1System(snmpEngine, 'krv_emerson_2', 'public')
        # Register SNMP Application at the SNMP engine
        ntfrcv.NotificationReceiver(snmpEngine, cbFun)
        # Run Twisted main loop
        reactor.run()
        print("The service not running, Start!!!")
        print(self.request)
    except CarrierError:
        print("The service is already running!!!")