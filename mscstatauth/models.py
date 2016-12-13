#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from mscstatapp.models import Mss

class User(AbstractUser):
    phone = models.CharField(max_length=11, verbose_name='Телефон основной',blank=True)
    phone_other = models.CharField(max_length=11, verbose_name='Телефон доп.',blank=True)
    phone_short = models.CharField(max_length=5, verbose_name='Короткий номер',blank=True)
    organization_name = models.CharField(max_length=100, verbose_name='Наименование организации',blank=True)
    business_address = models.CharField(max_length=100, verbose_name='Адрес места работы',blank=True)
    position = models.CharField(max_length=60, verbose_name='Должность',blank=True)
    birthday = models.DateField(verbose_name='Дата рождения',blank=True,null=True)
    mss = models.ManyToManyField(Mss,verbose_name='Филиал',blank=True)
    sms_notification = models.BooleanField(default=True,verbose_name='СМС оповещение')
    
    class Meta:
        ordering = ['last_name','first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
