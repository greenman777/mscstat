#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from Crypto.Cipher import Blowfish
import binascii
from django.db.models.signals import post_save
from rapidsms.router import send, lookup_connections
from smart_selects.db_fields import ChainedForeignKey


class Mss(models.Model):
    name = models.CharField(verbose_name = "коммутатор",max_length=30,db_index=True)
    title = models.CharField(verbose_name = "филиал",max_length=30,db_index=True,blank=True)
    port = models.IntegerField(verbose_name = "port",default=6000,blank=True)
    host = models.GenericIPAddressField(protocol='IPv4',verbose_name = "host",blank=True,null=True)
    login = models.CharField(verbose_name = "login",max_length=30,blank=True)
    password = models.CharField(verbose_name = "password",max_length=32,blank=True, editable=False)
    def get_crypto(self):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        return enc_obj.decrypt(binascii.a2b_hex(self.password)).rstrip().decode()
    def set_crypto(self, psw_value):
        enc_obj = Blowfish.new( settings.SECRET_KEY )
        repeat = 8 - (len( psw_value ) % 8)
        psw_value = psw_value + " " * repeat
        self.password = binascii.b2a_hex(enc_obj.encrypt( psw_value ))
    psw = property(get_crypto, set_crypto)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Филиалы"

class Object(models.Model):
    mss = models.ForeignKey(Mss,default=1,null=True)
    name = models.CharField(max_length=60,db_index=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Объекты"


class ObjectType(models.Model):
    object = models.ForeignKey(Object,null=True)
    name = models.CharField(max_length=60,db_index=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Тип объекта"


class Subscribes(models.Model):
    name = models.CharField(verbose_name = "Наименование подписки",max_length=30,blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Список подписок"


class SubscribeMessages(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Получатель',related_name='recipient')
    subscribe = models.ForeignKey(Subscribes,verbose_name = "Подписка",blank=True,null=True)
    mss = models.ForeignKey(Mss,verbose_name = "Филиал",blank=True,null=True)
    subscribe_active = models.BooleanField(default=True,verbose_name = "активная")
    def __unicode__(self):
            return self.subscribe.name
    class Meta:
        ordering = ['subscribe']
        verbose_name_plural = "Подписки на сообщения"


class Kpi(models.Model):
    name = models.CharField(verbose_name = "Наименование KPI",max_length=30,blank=True)
    higher_better = models.BooleanField(default=True,verbose_name = "выше лучше")
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "KPI"


class TkgThresholds(models.Model):
    mss = models.ForeignKey(Mss,verbose_name = "Коммутатор",blank=True,null=True)
    kpi = models.ForeignKey(Kpi,verbose_name = "KPI",blank=True,null=True)
    object_name = ChainedForeignKey(Object,verbose_name = "Объект мониторинга",chained_field="mss",chained_model_field="mss",show_all=False,auto_choose=True,blank=True,null=True)
    value_high = models.DecimalField(verbose_name = "высокий порог", max_digits=9,decimal_places=2,null=True,blank=True)
    value_sufficient = models.DecimalField(verbose_name = "достаточный порог", max_digits=9,decimal_places=2,null=True,blank=True)
    value_emergency = models.DecimalField(verbose_name = "аварийный порог", max_digits=9,decimal_places=2,null=True,blank=True)
    threshold_events = models.IntegerField(verbose_name = "число событий для достоверности",null=True,blank=True)
    threshold_active = models.BooleanField(default=True,verbose_name = "активный")
    def __unicode__(self):
            return self.kpi.name
    class Meta:
        ordering = ['kpi']
        verbose_name_plural = "Пороги TKG"


class Thresholds(models.Model):
    mss = models.ForeignKey(Mss,verbose_name = "Коммутатор",blank=True,null=True)
    kpi = models.ForeignKey(Kpi,verbose_name = "KPI",blank=True,null=True)
    value_high = models.DecimalField(verbose_name = "высокий порог", max_digits=9,decimal_places=2,null=True,blank=True)
    value_sufficient = models.DecimalField(verbose_name = "достаточный порог", max_digits=9,decimal_places=2,null=True,blank=True)
    value_emergency = models.DecimalField(verbose_name = "аварийный порог", max_digits=9,decimal_places=2,null=True,blank=True)
    percentage_reduction = models.DecimalField(default=0.0, verbose_name = "процент изменения порога", max_digits=4,decimal_places=2)
    threshold_events = models.IntegerField(verbose_name = "число событий для достоверности",null=True,blank=True)
    threshold_active = models.BooleanField(default=True,verbose_name = "активный")
    def __unicode__(self):
            return self.kpi.name
    class Meta:
        ordering = ['kpi']
        verbose_name_plural = "Пороги KPI"


class Unit(models.Model):
    name = models.CharField(max_length=60,db_index=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Разделы"


class Counter(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Счетчики"


class CounterNoCleaning(models.Model):
    counter = models.ForeignKey(Counter,verbose_name = "счетчик",blank=True,null=True)
    def __unicode__(self):
        return self.counter.name
    class Meta:
        ordering = ['counter']
        verbose_name_plural = "Список не удаляемых счетчиков"


class Counters(models.Model):
    mss = models.ForeignKey(Mss,verbose_name = "коммутатор",blank=True,null=True,db_index=True)
    unit = models.ForeignKey(Unit,verbose_name = "раздел",blank=True,null=True,db_index=True)
    object = models.ForeignKey(Object,verbose_name = "объект",blank=True,null=True,db_index=True)
    counter = models.ForeignKey(Counter,verbose_name = "счетчик",blank=True,null=True,db_index=True)
    counter_value = models.DecimalField(max_digits=9,decimal_places=2)
    datetime_start = models.DateTimeField(db_index=True)
    def __unicode__(self):
        return self.mss.title
    class Meta:
        ordering = ['datetime_start']
        verbose_name_plural = "Статистика"


class CommonPermissions(Mss):
    class Meta:
        proxy = True
        permissions = (("kpi_view","KPI view"),
                       ("totals_view","Totals view"),
                       ("reports_all_view","Reports all view"),
                       ("view_all_tasks", "View all tasks"))

class Priority(models.Model):
    name = models.CharField(max_length=30,verbose_name='Приоритет')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Пиоритет задачи"


class TaskStatus(models.Model):
    name = models.CharField(max_length=30,verbose_name='Статус задачи')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Статус задачи"


class Tasks(models.Model):
    priority = models.ForeignKey(Priority,verbose_name='Приоритет')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Автор',related_name='author')
    performer = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Исполнитель',related_name='performer')
    heading = models.CharField(max_length=80,verbose_name='Заголовок')
    description = models.CharField(max_length=160,verbose_name='Описание')
    create_date = models.DateField(verbose_name='Дата создания')
    execution_date = models.DateField(verbose_name='Дата выполнения')
    status = models.ForeignKey(TaskStatus,verbose_name='Статус')
    
    def __unicode__(self):
        return self.heading
    class Meta:
        ordering = ['create_date']
        verbose_name_plural = "Задачи"


class TaskHistory(models.Model):
    task = models.ForeignKey(Tasks,verbose_name='Задача')
    corrector = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Корректор')
    comment = models.CharField(max_length=100,verbose_name='Комментарий')
    create_date = models.DateField(verbose_name='Дата создания')
    status = models.ForeignKey(TaskStatus,verbose_name='Статус',related_name='status',)
    def __unicode__(self):
        return self.comment
    class Meta:
        ordering = ['pk']
        verbose_name_plural = "История задачи"


class TaskComments(models.Model):
    task = models.ForeignKey(Tasks,verbose_name='Задача')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Автор')
    comment = models.CharField(max_length=100,verbose_name='Комментарий')
    create_date = models.DateField(verbose_name='Дата создания')
    def __unicode__(self):
        return self.comment
    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Комментарии к задаче"


class Notifications(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user',verbose_name='Получатель')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sender',verbose_name='Отправитель',blank=True,null=True)
    date = models.DateTimeField(verbose_name='Дата операции',auto_now_add=True)
    message = models.CharField(max_length=150,verbose_name='Сообщение')
    read = models.BooleanField(default=False,verbose_name='Прочитано')
    sendsms = models.BooleanField(default=False,verbose_name='Отправлено SMS')
    def __unicode__(self):
        return self.message
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Уведомления"


def post_notifications_save(sender, instance, created, **kwargs):
    try:
        if (created):
            if (instance.user.sms_notification and (len(instance.user.phone)==11)):
                phone = "".join(("7",instance.user.phone[1:]))
                if instance.sendsms:
                    connections = lookup_connections(backend="kannel-beeline-smpp",identities=[phone])
                    send(instance.message, connections=connections)
    except (sender.DoesNotExist):
        return

post_save.connect(post_notifications_save, sender=Notifications)