#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mscstatapp.views.main import JSONResponse

def children(name="",iconcls=""):
    children = {"text":name,"leaf":False,"expanded":False,"children":[],"iconCls":iconcls}
    return children

def children_last(name,app="",filterapp="",hide_items="",title="",typeapp=""):
    children = {"text":name,"app":app,"filterapp":filterapp,"hide_items":hide_items,"title":title,"typeapp":typeapp,"leaf":True,"expanded":True,"children":None}
    return children

def menutree(request):
    
    user_id = request.user.id
    node_id = 0
    rootchildren = []
    
    """
    Дерево задач
    """
    rootchildren.append(children(name="Задачи",iconcls='icon-tasks'))
    rootchildren[node_id]["children"].append(children_last(name="Выполнить",app="appTasks",filterapp='{performer_id: '+str(user_id)+'}',
                                                           hide_items='{}',title='Выполнить',typeapp='tasks_make'))
    rootchildren[node_id]["children"].append(children_last(name="Проверить",app="appTasks",filterapp='{author_id: '+str(user_id)+'}',
                                                           hide_items='{}',title='Проверить',typeapp='tasks_check'))
    if request.user.has_perm('mscstatapp.view_all_task'):
        rootchildren[node_id]["children"].append(children_last(name="Все",app="appTasks",filterapp='{}',
                                                           hide_items='{}',title='Все задачи',typeapp='tasks_all'))
    node_id += 1
    nodechild_id = 0

    rootchildren.append(children(name="Статистика",iconcls='icon-statistics'))
    
    if request.user.has_perm('mscstatapp.kpi_view'):
            
        rootchildren[node_id]["children"].append(children(name="MSS"))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="CSetR",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='MSS CSetR',typeapp='mss_csetr'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="SucV",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='MSS SucV',typeapp='mss_sucv'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="mACR",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='MSS mACR',typeapp='mss_macr'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Calls",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='MSS Calls',typeapp='mss_calls'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="VLR",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='MSS VLR',typeapp='mss_vlr'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Inter-MSC HO",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='MSS Inter-MSC HO',typeapp='mss_intermscho'))
        nodechild_id += 1
        
        rootchildren[node_id]["children"].append(children(name="TKG"))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Load",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='TKG Load',typeapp='tkg_load'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Overflow",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='',title='TKG Overflow',typeapp='tkg_overflow'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="ACR in",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='TKG ACR in',typeapp='tkg_acr_in'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="SCR in",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='TKG SCR in',typeapp='tkg_scr_in'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="ACR out",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='TKG ACR out',typeapp='tkg_acr_out'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="SCR out",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='TKG SCR out',typeapp='tkg_scr_out'))
        nodechild_id += 1
        
        rootchildren[node_id]["children"].append(children(name="BSC-RNC"))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Load",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC Load',typeapp='bsc_load'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Overflow",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC Overflow',typeapp='bsc_overflow'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="ACR in",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC ACR in',typeapp='bsc_acr_in'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="SCR in",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC SCR in',typeapp='bsc_scr_in'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="ACR out",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC ACR out',typeapp='bsc_acr_out'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="SCR out",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='[]',title='BSC SCR out',typeapp='bsc_scr_out'))
        nodechild_id += 1
        
        rootchildren[node_id]["children"].append(children(name="IN"))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Fail",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='IN Fail',typeapp='in_fail'))
        rootchildren[node_id]["children"][nodechild_id]["children"].append(children_last(name="Abort",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',title='IN Abort',typeapp='in_abort'))
        nodechild_id += 1

    node_id += 1
    nodechild_id = 0
    
    rootchildren.append(children(name="Отчеты",iconcls='icon-reports'))

    if request.user.has_perm('mscstatapp.totals_view'):
        
        rootchildren[node_id]["children"].append(children_last(name="Общее время разговоров в день",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',
                                                                                         title='Общее время разговоров в день',typeapp='time_total'))
        rootchildren[node_id]["children"].append(children_last(name="Абоненты в VLR",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',
                                                                                         title='Абоненты в VLR',typeapp='vlrall_total'))
        rootchildren[node_id]["children"].append(children_last(name="Активные абоненты в VLR",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',
                                                                                         title='Активные абоненты в VLR',typeapp='vlratt_total'))
        rootchildren[node_id]["children"].append(children_last(name="Абонента в 2G",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',
                                                                                         title='Абонента в 2G',typeapp='vlr2g_total'))
        rootchildren[node_id]["children"].append(children_last(name="Абонента в 3G",app="appAdaptiveReport",
                                                                                         filterapp='{}', hide_items='["#objects"]',
                                                                                         title='Абонента в 3G',typeapp='vlr3g_total'))
        nodechild_id += 1
        
    
    serializer = {"children":rootchildren}
    response = JSONResponse(serializer)
    return response