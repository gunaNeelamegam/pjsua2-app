import pjsua2 as pj
from pjsua.pjsua2call import Pjsua2Call
from kivy.logger import Logger


class Pjsua2Account(pj.Account):
    def __init__(self, callback=lambda: print("Inside Pjsua2Account .......")):
        pj.Account.__init__(self)
        self.callback = callback

    def onRegState(self, prm: pj.OnRegStateParam):
        Logger.info("======== Account Registration ======== ")
        Logger.info(f"Registration Code ::  \t {prm.code}")
        Logger.info(f"Registration Status :: \t  {prm.status}")
        Logger.info(f"Registration Reason  :: \t  {prm.reason}")
        Logger.info(f"Registration Expiration :: \t {prm.expiration}")
        rData: pj.SipRxData = prm.rdata
        Logger.info(
            f""" 
            Registration srcAddress :: \t {rData.srcAddress} 
            Registration Info :: \t {rData.info} 
            Registaration Whole Message \t ::  {rData.wholeMsg}
            """
        )
        Logger.info("=" * 20)

    def onIncomingCall(self, prm: pj.OnIncomingCallParam):
        self.current_call: pj.Call = Pjsua2Call(self, prm.callId)
        current_call_info: pj.CallInfo = self.current_call.getInfo()
        Logger.info(f" {'='*10} :: Incoming Call {'='*10}")
        print(
            f"""
           Current Call Id :: \t {current_call_info.id} 
           Current Call Connection Duration :: \t  {current_call_info.connectDuration}
            
              """
        )
        call_prm: pj.CallOpParam = pj.CallOpParam(True)
        call_prm.statusCode = pj.PJSIP_SC_OK
        self.current_call.answer(call_prm)
        Logger.info(f"{'=' * 100}")

    def onInstantMessage(self, prm: pj.OnInstantMessageStatusParam):
        print("Instant Message:", prm)
        print("======== Incoming pager ======== ")
        print("From     : " + prm.thisown)
        print("To       : " + prm.toUri)
        print("Contact  : " + prm.reason)
        print("R Data :: ", prm.rdata)
        print("Code  :: ", prm.code)
        print("Body     : " + prm.msgBody)

    def onInstantMessageStatus(self, prm: pj.OnInstantMessageStatusParam):
        print("Instant Message Status:", prm)
        # Handle instant message status event

    def onTypingIndication(self, prm: pj.OnTypingIndicationParam):
        print("Typing Indication:", prm)
        # Handle typing indication event

    def onCallMediaTransportState(self, prm: pj.OnCallMediaTransportStateParam):
        print("Call Media Transport State:", prm)
        # Handle media transport state event

    def onCallState(self, prm: pj.OnCallStateParam):
        print("Call State:", prm)
        # Handle call state event

    def onCallMediaState(self, prm: pj.OnCallMediaStateParam):
        print("Call Media State:", prm)
        # Handle call media state event
