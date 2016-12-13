#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count,Sum,Max,Q
from datetime import datetime,timedelta
import time
from django.http import HttpResponse
from mscstatapp import models
from mscstatapp.views import main
import json
from mscstatapp.views.main import JSONResponse

def get_del_csetr(num1,num2):
    try:
        return round(float(1-float(num1)/float(num2))*100,2)
    except ZeroDivisionError:
        return 0

def get_del(num1,num2):
    try:
        return round((float(num1)/float(num2))*100,2)
    except ZeroDivisionError:
        return 0
    
def get_channel(num1,num2):
    if num1 == num2:
        return int(num1)
    if int(num1) == 0:
        return int(num2)
    if int(num2) == 0:
        return int(num1)
    
def get_rezult_zip(rezult_all,rezult):
    
    if len(rezult_all) == 0:
        rezult_all = rezult
    else:
        if len(rezult_all)<len(rezult):
            list_tmp = rezult_all[:]
            rezult_all = rezult[:]
            rezult = list_tmp
        for item_new in rezult:
            find_rec = False
            count = 0
            count_insert = -1
            for item in rezult_all:
                if (item['datetime_start'] > item_new['datetime_start']) and count_insert < 0:
                    count_insert = count
                if item['datetime_start']==item_new['datetime_start']:
                    item.update(item_new)
                    find_rec = True
                    break
                count += 1
            if not find_rec:
                if count_insert >= 0:
                    rezult_all.insert(count_insert,item_new)
                else:
                    rezult_all.append(item_new)
    return rezult_all

def check_kpi(kpi):
    mask_high = ['<FONT color="green">','</FONT>']
    mask_sufficient = ['<FONT color="blue">','</FONT>']
    mask_low = ['<FONT color="tomato">','</FONT>']
    mask_emergency = ['<FONT color="red">','</FONT>']
    for item_kpi in kpi['content']:
        mss = models.Mss.objects.get(title=item_kpi['filial'])
        thresholds = models.Thresholds.objects.filter(mss=mss)
        events = int(float(item_kpi['calls']))
        for threshold in thresholds:
            if item_kpi.get(threshold.kpi.name.lower()):
                value = float(item_kpi[threshold.kpi.name.lower()])
                value_emergency = threshold.value_emergency
                value_sufficient = threshold.value_sufficient
                value_high = threshold.value_high
                value_emergency_reduction = 0
                value_sufficient_reduction = 0
                value_high_reduction = 0
                if (events < threshold.threshold_events):
                    value_emergency_reduction = value_emergency * threshold.percentage_reduction /100.00
                    value_sufficient_reduction = value_sufficient * threshold.percentage_reduction /100.00
                    value_high_reduction = value_high * threshold.percentage_reduction /100.00
                if threshold.kpi.higher_better :
                    value_emergency = value_emergency - value_emergency_reduction
                    value_sufficient = value_sufficient - value_sufficient_reduction
                    value_high = value_high - value_high_reduction
                    if value <= value_emergency:
                        mask = mask_emergency
                        if threshold.threshold_active:
                            kpi['flag_alarm'] = True
                    elif value > value_emergency and value < value_sufficient:
                        mask = mask_low
                    elif value >= value_sufficient and value < value_high:
                        mask = mask_sufficient
                    elif value >= value_high:
                        mask = mask_high
                else:
                    value_emergency = value_emergency + value_emergency_reduction
                    value_sufficient = value_sufficient + value_sufficient_reduction
                    value_high = value_high + value_high_reduction
                    if value >= value_emergency:
                        mask = mask_emergency
                        if threshold.threshold_active:
                            kpi['flag_alarm'] = True
                    elif value < value_emergency and value > value_sufficient:
                        mask = mask_low
                    elif value <= value_sufficient and value > value_high:
                        mask = mask_sufficient
                    elif value <= value_high:
                        mask = mask_high
                item_kpi[threshold.kpi.name.lower()] = item_kpi[threshold.kpi.name.lower()].join(mask)
    return kpi


@csrf_exempt
def status(request=None,mss=None):
    
    DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    if mss == None:
        mss_all = models.Mss.objects.all()
    else:
        mss_all = [mss]
    kpi = {'content':[],'flag_alarm':False}
    for mss_id in mss_all:
        data = {}
        try:
            datetime_start = models.Counters.objects.filter(mss=mss_id).latest('datetime_start').datetime_start.strftime(DATETIME_FORMAT)
            data['date'] = datetime_start.split(" ")[0]
            data['time'] = datetime_start.split(" ")[1]
            
            data_csetr_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['Call_Connection_Traffic'],counter__name__in=['LAST-CHOICE_ROUTE_OVERFLOW_TIMES','CALL_FAIL_BECAUSE_OF_INTER-TRUNK_BUSY','CALL_FAIL_BECAUSE_OF_BSS-TRUNK_BUSY','CALL_FAIL_BECAUSE_OF_PEER_OFFICE_BUSY']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data_csetr_2 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['Call_Connection_Traffic'],counter__name__in=['CALL_ATTEMPT_TIMES']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data['csetr'] = "%.2f" % get_del_csetr(data_csetr_1,data_csetr_2)
            
            data_sucv_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['Incoming_Calls_and_Local_Originated_Calls'],counter__name__in=['Incoming_Answer_Times','Incoming_User_Busy_Times','Incoming_Call_Releases_After_Ringing','Incoming_Call_Releases_Before_Ringing','Incoming_Callee_No_Answer_Times','Originated_Answer_Times','Originated_User_Determined_User_Busy_Times','Originated_Network_Determined_Busy_Times','Originated_Releases_Before_Ringing','Originated_No_Answer_After_Ringing']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"] 
            data_sucv_2 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['Incoming_Calls_and_Local_Originated_Calls'],counter__name__in=['Incoming_Seizure_Times','Originated_Call_Attempts']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"] 
            data['sucv'] = "%.2f" % get_del(data_sucv_1,data_sucv_2)
            
            data_macr_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Answer_Times','2G_TERMINATED_ANSWER','3G_TERMINATED_ANSWER']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"] 
            data_macr_2 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Call_Attempts','2G_TERMINATED_CALL_ATTEMPT','3G_TERMINATED_CALL_ATTEMPT']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data['macr'] = "%.2f" % get_del(data_macr_1,data_macr_2)
            
            data_calls_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Call_Attempts','2G_TERMINATED_CALL_ATTEMPT','3G_TERMINATED_CALL_ATTEMPT']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data['calls'] = "%.2f" % data_calls_1
            
            data_fail_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['IN_Failures'],counter__name__in=['Call_Rejections_due_to_Overload','Call_Failures_Before_InitialDP','Call_Failures_After_InitialDP','Number_of_REJECT_Primitives_Received_by_SSF_Modules']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data['in_fail'] = "%.2f" % data_fail_1
            
            data_abort_1 = models.Counters.objects.filter(mss=mss_id, unit__name__in=['IN_Dialogs'],counter__name__in=['SSF_Sending_Dialog_Abort_Times','SSF_Receiving_Dialog_Abort_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')).latest('datetime_start')["calls_value"]
            data['in_abort'] = "%.2f" % data_abort_1
            
            data["filial"]=mss_id.title
            kpi["content"].append(data.copy())

        except models.Counters.DoesNotExist:
            pass
    if mss == None:
        return JSONResponse(check_kpi(kpi))
    else:
        return check_kpi(kpi)

@csrf_exempt
def reports(request):
    
    DATETIME_FORMAT = "%Y-%m-%d %H:%M"
    
    if request.method == 'POST':
        getparams = request.POST.copy()
        report_type =  getparams.get('report_type')
        datetime_start =  datetime.strptime(getparams.get('datetime_start'), DATETIME_FORMAT)
        datetime_stop =  datetime.strptime(getparams.get('datetime_stop'), DATETIME_FORMAT)
        mss_id = int(getparams.get('mss_id'))
        objects_id = json.loads(request.POST['objects_id'])
        title = getparams.get('title')
        data = {'success':True,'messages':[]}
        fields = []
        rezult_all = []
        qs = models.Counters.objects.filter(datetime_start__range=(datetime_start,datetime_stop),mss=mss_id)[:]
        if len(objects_id)==0:
            objects_id = main.get_object_list(mss_id,report_type)

        if report_type == "mss_csetr":
            data_1 = qs.filter(unit__name__in=['Call_Connection_Traffic'],counter__name__in=['LAST-CHOICE_ROUTE_OVERFLOW_TIMES','CALL_FAIL_BECAUSE_OF_INTER-TRUNK_BUSY','CALL_FAIL_BECAUSE_OF_BSS-TRUNK_BUSY','CALL_FAIL_BECAUSE_OF_PEER_OFFICE_BUSY']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
            data_2 = qs.filter(unit__name__in=['Call_Connection_Traffic'],counter__name__in=['CALL_ATTEMPT_TIMES']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'csetr': get_del_csetr(data_1['calls_value'],data_2['calls_value'])} for data_1, data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['csetr'],'data':rezult})
        
        if report_type == "mss_sucv":
            data_1 = qs.filter(unit__name__in=['Incoming_Calls_and_Local_Originated_Calls'],counter__name__in=['Incoming_Answer_Times','Incoming_User_Busy_Times','Incoming_Call_Releases_After_Ringing','Incoming_Call_Releases_Before_Ringing','Incoming_Callee_No_Answer_Times','Originated_Answer_Times','Originated_User_Determined_User_Busy_Times','Originated_Network_Determined_Busy_Times','Originated_Releases_Before_Ringing','Originated_No_Answer_After_Ringing']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
            data_2 = qs.filter(unit__name__in=['Incoming_Calls_and_Local_Originated_Calls'],counter__name__in=['Incoming_Seizure_Times','Originated_Call_Attempts']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'sucv': get_del(data_1['calls_value'],data_2['calls_value'])} for data_1, data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['sucv'],'data':rezult})
        
        if report_type == "mss_macr":
            data_1 = qs.filter(unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Answer_Times','2G_TERMINATED_ANSWER','3G_TERMINATED_ANSWER']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
            data_2 = qs.filter(unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Call_Attempts','2G_TERMINATED_CALL_ATTEMPT','3G_TERMINATED_CALL_ATTEMPT']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'macr': get_del(data_1['calls_value'],data_2['calls_value'])} for data_1, data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['macr'],'data':rezult})
        
        if report_type == "mss_calls":
            data_1 = qs.filter(unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Call_Attempts','2G_TERMINATED_CALL_ATTEMPT','3G_TERMINATED_CALL_ATTEMPT']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'calls': data_1['calls_value']} for data_1 in data_1]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['calls'],'data':rezult})
        
        if report_type == "mss_vlr":
            data_1 = qs.filter(unit__name__in=['Number_of_VLR_Subscribers'],counter__name__in=['Number_of_Local_Subscribers_in_VLR','Number_of_Roaming_Subscribers_in_VLR']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['Number_of_VLR_Subscribers'],counter__name__in=['Number_of_IMSI_Attached_Subscribers_in_VLR']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_3= qs.filter(unit__name__in=['Number_of_VLR_Subscribers'],counter__name__in=['Number_of_Roaming_Subscribers_in_VLR']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'vlrsubsc': data_1['calls_value'],'vlrattach': data_2['calls_value'],'vlrroumers': data_3['calls_value']} for data_1,data_2,data_3 in zip(data_1,data_2,data_3)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['vlrsubsc','vlrattach','vlrroumers'],'data':rezult})

        if report_type == "in_fail":
            data_1 = qs.filter(unit__name__in=['IN_Failures'],counter__name__in=['Call_Rejections_due_to_Overload','Call_Failures_Before_InitialDP','Call_Failures_After_InitialDP','Number_of_REJECT_Primitives_Received_by_SSF_Modules']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'fail': data_1['calls_value']} for data_1 in data_1]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['fail'],'data':rezult})
        
        if report_type == "in_abort":
            data_1 = qs.filter(unit__name__in=['IN_Dialogs'],counter__name__in=['SSF_Sending_Dialog_Abort_Times','SSF_Receiving_Dialog_Abort_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'abort': data_1['calls_value']} for data_1 in data_1]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['abort'],'data':rezult})
        
        if report_type == "mss_intermscho":
            if len(objects_id) != 0:
                data_output_1 = qs.filter(unit__name__in=['GSM_Cell_Handover'],object__in=objects_id,counter__name__in=['Successful_Inter-MSC_Handover_from_Cell_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_output_2 = qs.filter(unit__name__in=['GSM_Cell_Handover'],object__in=objects_id,counter__name__in=['Inter-MSC_Handover_from_Cell_Requested_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_input_1 = qs.filter(unit__name__in=['GSM_Cell_Handover'],object__in=objects_id,counter__name__in=['Successful_Inter-MSC_Handover_to_Cell_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_input_2 = qs.filter(unit__name__in=['GSM_Cell_Handover'],object__in=objects_id,counter__name__in=['Inter-MSC_Handover_to_Cell_Requested_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            else:
                data_output_1 = qs.filter(unit__name__in=['GSM_Cell_Handover'],counter__name__in=['Successful_Inter-MSC_Handover_from_Cell_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_output_2 = qs.filter(unit__name__in=['GSM_Cell_Handover'],counter__name__in=['Inter-MSC_Handover_from_Cell_Requested_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_input_1 = qs.filter(unit__name__in=['GSM_Cell_Handover'],counter__name__in=['Successful_Inter-MSC_Handover_to_Cell_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_input_2 = qs.filter(unit__name__in=['GSM_Cell_Handover'],counter__name__in=['Inter-MSC_Handover_to_Cell_Requested_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_output_1['datetime_start'].timetuple())*1000,'HO_output': get_del(data_output_1['calls_value'],data_output_2['calls_value']),'HO_input': get_del(data_input_1['calls_value'],data_input_2['calls_value'])} for data_output_1,data_output_2,data_input_1,data_input_2 in zip(data_output_1,data_output_2,data_input_1,data_input_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['HO_output','HO_input'],'data':rezult})
        
        if report_type == 'vlrall_total':
            data_1 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)','Local_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)','Local_Subscribers_(RNC)','Roaming_Subscribers_(BSC)','Roaming_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'Local 2G+3G': data_1['calls_value'],'Total 2G+3G': data_2['calls_value']} for data_1,data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['Local 2G+3G','Total 2G+3G'],'data':rezult})
        
        if report_type == 'vlratt_total':
            data_1 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)','Local_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)','Local_Subscribers_(RNC)','Roaming_Subscribers_(BSC)','Roaming_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_3 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Power-off_Subscribers_(BSC)','Power-off_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_4 = qs.filter(unit__name__in=['BSC_Traffic_Distribution','RNC_Traffic_Distribution'],counter__name__in=['Power-off_Subscribers_(BSC)','Power-off_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'Local 2G+3G': data_1['calls_value']-data_3['calls_value'],'Total 2G+3G': data_2['calls_value']-data_4['calls_value']} for data_1,data_2,data_3,data_4 in zip(data_1,data_2,data_3,data_4)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['Local 2G+3G','Total 2G+3G'],'data':rezult})
        
        if report_type == 'vlr2g_total':
            data_1 = qs.filter(unit__name__in=['BSC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['BSC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(BSC)','Roaming_Subscribers_(BSC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'Local 2G': data_1['calls_value'],'Total 2G': data_2['calls_value']} for data_1,data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['Local 2G','Total 2G'],'data':rezult})
        
        if report_type == 'vlr3g_total':
            data_1 = qs.filter(unit__name__in=['RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['RNC_Traffic_Distribution'],counter__name__in=['Local_Subscribers_(RNC)','Roaming_Subscribers_(RNC)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'Local 3G': data_1['calls_value'],'Total 3G': data_2['calls_value']} for data_1,data_2 in zip(data_1,data_2)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['Local 3G','Total 3G'],'data':rezult})
        
        if report_type == 'time_total':
            data_1 = qs.filter(unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls','UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Answer_Traffic','2G_TERMINATED_ANSWER_USAGE','3G_TERMINATED_ANSWER_USAGE']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_2 = qs.filter(unit__name__in=['GSM_Subscriber_Originated_Calls','GSM_Subscriber_Terminated_Calls'],counter__name__in=['Answer_Traffic','2G_TERMINATED_ANSWER_USAGE']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            data_3 = qs.filter(unit__name__in=['UTRAN_Subscriber_Originated_Calls','UTRAN_Subscriber_Terminated_Calls'],counter__name__in=['Answer_Traffic','3G_TERMINATED_ANSWER_USAGE']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
            rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000,'Total 2G+3G': data_1['calls_value'],'Total 2G': data_2['calls_value'],'Total 3G': data_3['calls_value']} for data_1,data_2,data_3 in zip(data_1,data_2,data_3)]
            data["messages"].append({'chart_id':report_type,'title':title,'fields':['Total 2G+3G','Total 2G','Total 3G'],'data':rezult})
        
        if report_type == 'tkg_acr_in':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Answer_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'tkg_acr_out':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Answer_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'tkg_scr_in':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Call_Completion_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'tkg_scr_out':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Call_Completion_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'tkg_overflow':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Traffic_in_Trunk_Office_Directions'],object=obj).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: data_1['calls_value']} for data_1 in data_1]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'tkg_load':
            fields = ['Sum','In','Out','AvCh','Inst'];
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                data_sum = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups','Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_in = qs.filter(unit__name__in=['Incoming_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_out = qs.filter(unit__name__in=['Outgoing_Calls_through_Trunk_Groups'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                if len(data_in)==0:
                    data_in = [{'calls_value': 0.0, 'datetime_start': item['datetime_start']} for item in data_out]
                if len(data_out)==0:
                    data_out = [{'calls_value': 0.0, 'datetime_start': item['datetime_start']} for item in data_in]
                data_avch_in = qs.filter(unit__name__in=['Trunk_Group_Traffic'],object=obj,counter__name__in=['Number_of_Available_Circuits_for_Incoming_Calls']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_avch_out = qs.filter(unit__name__in=['Trunk_Group_Traffic'],object=obj,counter__name__in=['Number_of_Available_Circuits_for_Outgoing_Calls_(Trunk_Group)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_inst_in = qs.filter(unit__name__in=['Trunk_Group_Traffic'],object=obj,counter__name__in=['Number_of_Installed_Circuits_for_Incoming_Calls_(Trunk_Group)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_inst_out = qs.filter(unit__name__in=['Trunk_Group_Traffic'],object=obj,counter__name__in=['Number_of_Installed_Circuits_for_Outgoing_Calls_(Trunk_Group)']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_sum['datetime_start'].timetuple())*1000, 'Sum': data_sum['calls_value'],'In': data_in['calls_value'],'Out': data_out['calls_value'],'AvCh': get_channel(data_avch_in['calls_value'],data_avch_out['calls_value']),'Inst': get_channel(data_inst_in['calls_value'],data_inst_out['calls_value'])} for data_sum,data_in,data_out,data_avch_in,data_avch_out,data_inst_in,data_inst_out in zip(data_sum,data_in,data_out,data_avch_in,data_avch_out,data_inst_in,data_inst_out)]
                data["messages"].append({'chart_id':obj_name,'title':obj_name,'fields':fields,'data':rezult[:]})

        if report_type == 'bsc_acr_in':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Answer_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'bsc_acr_out':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Answer_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'bsc_scr_in':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Call_Completion_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'bsc_scr_out':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Call_Completion_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'bsc_overflow':
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                fields.append(obj_name)
                data_1 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Overflow_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value')) 
                data_2 = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Times']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_1['datetime_start'].timetuple())*1000, obj_name: get_del(data_1['calls_value'],data_2['calls_value'])} for data_1,data_2 in zip(data_1,data_2)]
                rezult_all = get_rezult_zip(rezult_all,rezult)
            data["messages"].append({'chart_id':report_type,'title':title,'fields':fields,'data':rezult_all})
        
        if report_type == 'bsc_load':
            fields = ['Sum','In','Out','AvCh','Inst'];
            for obj in objects_id:
                obj_name = models.Object.objects.get(id=obj).name
                obj_name = obj_name[:obj_name.find('(')];
                data_sum = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions','Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_in = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_out = qs.filter(unit__name__in=['Outgoing_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Seizure_Traffic']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_avch = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Number_of_Available_Circuits']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                data_inst = qs.filter(unit__name__in=['Incoming_Calls_in_Mobile_Office_Directions'],object=obj,counter__name__in=['Number_of_Installed_Circuits']).values('datetime_start').annotate(calls_value=Sum('counter_value'))
                rezult = [{'datetime_start': time.mktime(data_sum['datetime_start'].timetuple())*1000, 'Sum': data_sum['calls_value'],'In': data_in['calls_value'],'Out': data_out['calls_value'],'AvCh': data_avch['calls_value'],'Inst': data_inst['calls_value']} for data_sum,data_in,data_out,data_avch,data_inst in zip(data_sum,data_in,data_out,data_avch,data_inst)]
                data["messages"].append({'chart_id':obj_name,'title':obj_name,'fields':fields,'data':rezult[:]})

    response = JSONResponse(data)
    return response
