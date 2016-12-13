from __future__ import unicode_literals
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
import struct, datetime

def watch_start():
    
    transportDispatcher = AsynsockDispatcher()
    transportDispatcher.registerRecvCbFun(cbFun)
    transportDispatcher.registerTransport(udp.domainName, udp.UdpSocketTransport().openServerMode(('localhost', 162)))
    transportDispatcher.jobStarted(1)
    try:
        transportDispatcher.runDispatcher()
    except:
        pass
        
def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):

    AlarmStatusChange = {"1":"activated", "2":"deactivated"}
    AlarmSeverity = {"3":"warning", "4":"minor", "5":"magor", "6":"critical"}
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if api.protoModules.has_key(msgVer):
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version')
            return
        reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message(),)
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            data_mess = {"DeviceType":"", "AlarmTrapNo":"", "AlarmTime":"", "AlarmStatusChange":"", "AlarmSeverity":"", "AlarmDescription":"", "AlarmType":""}
            if msgVer == api.protoVersion1:
                data_mess["DeviceType"] = "Conditioner"              
                data_mess["AlarmDescription"] = pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()
                data_mess["AlarmTime"] = datetime.datetime.now().strftime(DATETIME_FORMAT)
                data_mess["AlarmSeverity"] = pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint() 
                data_mess["AlarmStatusChange"] = "activated"
            else:
                mess_trap = pMod.apiPDU.getVarBindList(reqPDU)               
                try:
                    data_mess["DeviceType"] = "Power"
                    data_mess["AlarmTrapNo"] = mess_trap.getComponentByPosition(2).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(1).getComponentByPosition(1) 
                    dt_raw = str(mess_trap.getComponentByPosition(3).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(0).getComponentByPosition(1))                
                    dt = datetime.datetime(*struct.unpack('>HBBBBBB', dt_raw[:-3]))	
                    data_mess["AlarmTime"] = dt.strftime(DATETIME_FORMAT)
                    status = str(mess_trap.getComponentByPosition(4).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(0).getComponentByPosition(0)) 
                    if AlarmStatusChange.get(status) is not None:
                        data_mess["AlarmStatusChange"] = AlarmStatusChange[status]
                    severity = str(mess_trap.getComponentByPosition(5).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(0).getComponentByPosition(0)) 
                    if AlarmSeverity.get(severity) is not None:
                        data_mess["AlarmSeverity"] = AlarmSeverity[severity]
                    data_mess["AlarmDescription"] = mess_trap.getComponentByPosition(6).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(0).getComponentByPosition(1)
                    data_mess["AlarmType"] = mess_trap.getComponentByPosition(7).getComponentByPosition(1).getComponentByPosition(0).getComponentByPosition(0).getComponentByPosition(0)
                    print(data_mess)
                except AttributeError:
                    pass
            
    return wholeMsg
       
    def watch_stop():
        
        transportDispatcher.jobFinished(1)
        transportDispatcher.closeDispatcher()
