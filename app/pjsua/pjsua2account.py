import pjsua2 as pj
from pjsua.pjsua2call import Pjsua2Call
from kivy.logger import Logger
import time
class Pjsua2Account(pj.Account):

    """
    please note current call in this context that points to incoming call.
    Getting access on current incomming call instance

    Note:
        * 2 way's of accessing the current call instance using account class instance and using the class variable

    way we accessing the current call instance:

        using Static member's (or) using class Variable
    """

    incoming_call = None

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
        try:
            super(Pjsua2Call, self).onCallState(prm)
            callinfo: pj.CallInfo = self.getInfo()
            call_state = callinfo.state
            call_id = callinfo.id
            Logger.info(f"{'='*10} :: Call State In Account :: {'='*10}")
            if call_state == pj.PJSIP_INV_STATE_CALLING:
                self.start_time = time.time()
            elif call_state in (
                pj.PJSIP_INV_STATE_DISCONNECTED,
                pj.PJSIP_INV_STATE_NULL,
            ):
                self.end_time = time.time()
                duration = self.calculateDuration()
                Logger.info(
                    f"Call ID: {call_id}, Duration: {duration} seconds {duration/60}"
                )
            Logger.info(
                f"""
                       Call State :: \t {callinfo.state}
                       Call Status Text :: \t {callinfo.stateText}
                       Call Info  :: \t  {callinfo.remVideoCount}
                        """
            )
            Logger.info("=" * 50)
        except Exception as e:
            Logger.error(e.args)

    def onCallMediaState(self, prm: pj.OnCallMediaStateParam):
        print("Call Media State:", prm)
        # Handle call media state event
