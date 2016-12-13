
# Callback function for receiving notifications
from __future__ import unicode_literals

def cbFun(snmpEngine,stateReference,contextEngineId, contextName,varBinds,cbCtx):
    (transportDomain,transportAddress) = snmpEngine.msgAndPduDsp.getTransportInfo(stateReference)

    print('Notification from %s, ContextEngineId "%s", ContextName "%s"' % (
        transportAddress, contextEngineId.prettyPrint(),
        contextName.prettyPrint()
    ))
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))