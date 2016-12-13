#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from mscstatapp import models
from mscstatauth.models import User
from django.http import HttpResponse
import base64
import unicodecsv,csv
import json
from datetime import datetime
from rest_framework.renderers import JSONRenderer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

OBJECTTYPE_NAME = {
    'tkg_load':['Incoming_or_bidirection_trunk_group','Outgoing_or_bidirection_trunk_group','Trunk_group'],
    'tkg_overflow':['Trunk_Office_Direction'],
    'tkg_acr_in':['Incoming_or_bidirection_trunk_group'],
    'tkg_scr_in':['Incoming_or_bidirection_trunk_group'],
    'tkg_acr_out':['Outgoing_or_bidirection_trunk_group'],
    'tkg_scr_out':['Outgoing_or_bidirection_trunk_group'],
    'bsc_load':['RNC_or_BSC_Office_Direction'],
    'bsc_overflow':['RNC_or_BSC_Office_Direction'],
    'bsc_acr_in':['RNC_or_BSC_Office_Direction'],
    'bsc_scr_in':['RNC_or_BSC_Office_Direction'],
    'bsc_acr_out':['RNC_or_BSC_Office_Direction'],
    'bsc_scr_out':['RNC_or_BSC_Office_Direction'],
    'mss_intermscho':['GSM_GCI'],
}

@login_required
def mainpage(request):
    user_groups = request.user.groups.values_list('id',flat=True)
    return render_to_response('index.html',{'user_groups':user_groups},RequestContext(request))

def auction(request):
    return render_to_response('auction.html')

def get_object_list(mss,typeapp):
    mss = mss
    typeapp = typeapp
    if typeapp.startswith('tkg_'):
        filterobj = models.Object.objects.filter(mss=mss,objecttype__name__in=OBJECTTYPE_NAME[typeapp]).exclude(name__contains='NULL').exclude(name__contains='BSC').values_list('id', flat=True).order_by('id').distinct()
    elif typeapp.startswith('bsc_'):
        filterobj = models.Object.objects.filter(mss=mss,objecttype__name__in=OBJECTTYPE_NAME[typeapp]).exclude(name__contains='NULL').filter(name__contains='BSC').values_list('id', flat=True).order_by('id').distinct()
    elif typeapp.startswith('mss_intermscho'):
        filterobj = models.Object.objects.filter(mss=mss,objecttype__name__in=OBJECTTYPE_NAME[typeapp]).exclude(name__contains='NULL').values_list('id', flat=True).order_by('id').distinct()
    else:
        filterobj = []
    return filterobj

@csrf_exempt
def down_chart(request):
    if request.method == 'POST':
        getparams = request.POST.copy()
        png_data =  getparams.get('data')
        if png_data != None:
            png_str = png_data.partition('base64,')[2]
            png_result = base64.b64decode(png_str)
            response = HttpResponse(png_result,content_type='image/png')
            response['Content-Disposition']='attachment; filename="chart.png"'
            return response

@csrf_exempt
def notifications_news(request):
    if request.method == 'POST':
        user = request.user
        if user != None:
            count_news = 0
            response = JSONResponse({'success':True,
                                     'messages':{
                                        'count_news':count_news,
                                      }
                                   })
            return response
        
@csrf_exempt
def send_notification(request):
    if request.method == 'POST':
        getparams = request.POST.copy()
        recipients =  json.loads(getparams.get('recipients'))
        message =  getparams.get('message')
        sendsms =  json.loads(getparams.get('sendsms'))
        if len(recipients) == 0:
            recipients = User.objects.filter(is_active=True)
        else:
            recipients = [User.objects.get(id=recipient) for recipient in recipients]
        for recipient in recipients:
            models.Notifications.objects.create(user=recipient,sender=request.user,message=message,sendsms=sendsms)
        response = JSONResponse({'success':True,'messages':'Сообщение успешно отправлено!'})
        return response

@csrf_exempt
def export_csv(request):
    if request.method == 'POST':
        getparams = request.POST.copy()
        data =  json.loads(getparams.get('data_raw'))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=export_chart.csv'
        writer = unicodecsv.writer(response,delimiter=';',encoding='cp1251')
        if len(data)>0:
            del data[0]['id']
            headers = [header for header in data[0].keys()]
            writer.writerow(headers)
            for row in data:
                try:
                    del row['id']
                except KeyError:
                    pass
                for key in row.keys():
                    row[key] = str(row[key]).replace('.',',')
                row['datetime_start'] = datetime.fromtimestamp(float(row['datetime_start'])/1000).strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([row[key] for key in headers])
        return response 