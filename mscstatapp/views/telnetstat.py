#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telnetlib, socket, time, re
import datetime

def telnet_exec(host, port, login, password, buffer):
    results = []
    ser = socket.gethostbyname_ex(socket.gethostname())[2][0] + "---O&M System"
    try:
        tn = telnetlib.Telnet(host, port)
        tn.write("".join(('LGI:op="',login,'",pwd="',password,'",ser="',ser,'";\n')))
        buf = tn.read_until(b"---    END").encode('ascii')
        status = "Unknown error"
        if buf.find("logged in successfully") >=0:
            status = "Logged successfully"
            tn.write(buffer);
            while True:
                buf = tn.read_until(b"---    END").encode('ascii')
                if buf and buf.find("reports in total") and buf.find("To be continued...") >= 0:
                    results.append(buf)
                else:
                    results.append(buf)
                    break
        else:
            status = "Logged failure"
        tn.close()
        return status,results
    except socket.error as err:
        status = "Connect failure"
        return status,results

def reply_parser(report):
        
    if report.find("reports in total") == "LST ALMAF":
        data = {"type":"alarm", "message":"", "phone":""}
        alarm = {"Sync serial No.":"", "Alarm name":"", "Alarm raised time":"", "Location info":""}
        message = ""
        list_alarm = []
        param_value = ""  
        flag_alarm = False
        for string in report.splitlines():
            if string.find("Module No.") >= 0:
                flag_alarm = False
                list_alarm.append(alarm.copy())
            if flag_alarm == True:
                if string.find("  =  ") >= 0:
                    param_value = ""
                    param_name = string.split("  =  ")[0].strip()
                    param_value = string.split("  =  ")[1].strip()
                else:
                    param_value = param_value + " " + string
                if alarm.get(param_name) != None:
                    alarm[param_name] = param_value
            if string.find("ALARM") >= 0:
                flag_alarm = True
        for alm in list_alarm:
            alm_time = alm["Alarm raised time"][:16]
            if len(list_alarm) > 1 and len(list_alarm) <= 5:
                message = message + alm_time + " = " + alm["Alarm name"] + ", " + alm["Sync serial No."] + "\n"
            if len(list_alarm) > 5:
                message = message + alm_time + " = " + alm["Sync serial No."] + "\n"
            elif len(list_alarm) == 1:
                message = message + alm_time + " = " + alm["Alarm name"] + ", info: " + alm["Location info"] + "\n"
        if len(message) > 0:     
            data["message"] = message
        else:
            data["message"] = "no alarms"
        
    if report.find("LST TRFRPT:") >=0 :
        try:
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            mss_name = re.search(r"\+{3} {4}(?P<mssname>\w+)(?<![ \t])", report).group("mssname")
            unit_name = re.search(r"(?m)MeasureUnit (?P<unitname>.*)$", report).group("unitname").strip().replace(" ", "_")
            try:
                match = re.search(r"(?m)(?P<object_type>Trunk group|Incoming or bidirection trunk group|Outgoing or bidirection trunk group|Bear service type|  GCI|Connection type|Service key|RNC or BSC Office Direction|GSM GCI|Trunk Office Direction|BSC|RNC) {2}(?P<object_name>.*)$", report)
                object_name = match.group("object_name").strip()
                if unit_name == "Traffic_Measurement_For_GCI":
                    try:
                        object_name = str(int(re.search(r"\((?P<name>[\w]+)\)", object_name).group("name").strip()[-4:],16))
                    except AttributeError:
                        object_name = "empty"
                object_type = match.group("object_type").strip().replace(" ", "_")
            except AttributeError:
                object_name = "empty"
                object_type = "empty"
            match = re.search(r"(?m)MeasurePeriod (?P<interval>.*) (minute|minutes|hour|day).*StartTime (?P<date_time>.*)(?P<tzone>(\+|\-).*):", report)
            date_time = match.group("date_time")
            tzone = match.group("tzone").replace('+', '-').replace('-', '+')
            datetime_start = datetime.datetime(*time.strptime(date_time, DATETIME_FORMAT)[0:6]).strftime(DATETIME_FORMAT)
            kpi_list = []
            kpi_item = {"mss_name":mss_name,"unit_name":unit_name,"object_name":object_name,"object_type":object_type,"datetime_start":datetime_start,"tzone":tzone}
            counters = re.compile(r'^ ([\w\(\)\-\_ ]+) {2}([\d\.]+)',re.MULTILINE).findall(report[report.rfind('Accuracy Of Result'):])
            for counter in counters:
                kpi_item["counter_name"] = counter[0].strip().replace(" ", "_")
                kpi_item["counter_value"] = counter[1]
                kpi_list.append((kpi_item).copy())
            return kpi_list
        except AttributeError:
            print(report)
            return []
    if report.find("LST TRFINF:") >=0 :
        tasks = re.findall(r'TaskName  =  (STAT_[\w\_]+)',report)
        return tasks