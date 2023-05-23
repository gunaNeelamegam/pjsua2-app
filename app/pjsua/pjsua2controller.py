"""
Main Application 

"""

import pjsua2 as pj
from utils.config import load_to_instance
from pjsua.pjsua2account import Pjsua2Account
from pjsua.pjsua2endpoint import Pjsua2Endpoint
from pjsua.pjsua2call import Pjsua2Call
from kivy.logger import Logger
from kivy.clock import Clock

class AccountException(Exception):
    """
    Account Exception
    """


class PJSUA2Controller:

    """
    PJSUA2 APP
    """

    def print_pad(message, prefix="*") -> None:
        return Logger.info(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self, file_name: str = "config.yaml") -> None:
        """
        Initailzing the pjsua2 application.

        Make Sure:
            Endpoint must be create only ones in application.

        """
        load_to_instance(file_name, instance=self)
        self.init_endpoint()
        self.init_transport()
        self.ep.libStart()
        self.set_accountconfig()
        self.create_account()
        Clock.schedule_interval(lambda *args :self.make_call(),10)
        """
        Must call only ones inside the entitre application context 
        """

    def init_endpoint(self):
        """
        method initalizing the endpoint one's inside application
        """

        log = pj.LogConfig()
        log.consoleLevel = 4
        log.level = 4
        self.ep_cfg: pj.EpConfig = pj.EpConfig()
        self.ep = Pjsua2Endpoint()
        try:
            self.ep.libCreate()
        except Exception as e:
            self.print_pad(e.args)
            return

        """
         Endpoint User Configaration 
        
        """

        self.ua_config: pj.UaConfig = self.ep_cfg.uaConfig
        self.ua_config.threadCnt = 0
        self.ua_config.maxCalls = 10
        self.ep.libInit(self.ep_cfg)

        """
            Endpoint Media Configration's
        """
        self.media_config: pj.MediaConfig = self.ep_cfg.medConfig
        self.media_config.sndClockRate = 16000
        Logger.info("============ Media port's user endpoint configration =========")

    def init_transport(self):
        try:
            self.sipTpConfig: pj.TransportConfig = pj.TransportConfig()
            self.sipTpConfig.port = self.port
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, self.sipTpConfig)
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_UDP6, self.sipTpConfig)
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_TCP, self.sipTpConfig)
            self.ep.transportCreate(3, self.sipTpConfig)

        except Exception as e:
            self.print_pad(e.args)

    def set_accountconfig(self):
        try:
            self.acfg: pj.AccountConfig = pj.AccountConfig()
            self.acfg.idUri = f"sip:{self.name}@{self.ip}"
            self.acfg.regConfig.registrarUri = f"sip:{self.ip}"
            self.cred: pj.AuthCredInfo = pj.AuthCredInfo(
                "digest", "*", f"{self.name}", 0, f"{self.password}"
            )

            ### Account Configaration

            self.natconfig: pj.AccountNatConfig = self.acfg.natConfig
            self.natconfig.iceEnabled = True
            self.videoconfig: pj.AccountVideoConfig = self.acfg.videoConfig
            self.videoconfig.autoShowIncoming = True
            self.videoconfig.autoTransmitOutgoing = True

            self.mediaconfig: pj.AccountMediaConfig = self.acfg.mediaConfig
            self.mediaconfig.srtpUse = True
            self.mediaconfig.srtpSecureSignaling = 0

            ## Sip configaration
            self.sipconfig: pj.AccountSipConfig = self.acfg.sipConfig
            self.sipconfig.authCreds.append(self.cred)

        except Exception as e:
            self.print_pad(e)

    def create_account(self):
        try:
            self.acc: pj.Account = Pjsua2Account()
            self.acc.create(
                self.acfg,
            )
        except AccountException as ace:
            self.print_pad(ace.args)

    def clean_up(self):
        """
        cleanup method:
            clean the pjsua2 memory

        """
        self.ep.transportShutdown(self)
        self.acc.shutdown()
        self.ep.libDestroy()
        self.print_pad("Application Shutdown's", prefix="#")

    def make_call(self):
        self.call = Pjsua2Call(self.acc, 0)
        self.call.makeCall(f"sip:6001@{self.ip}", pj.CallOpParam(True))

    def __enter__():
        pass

    def __exit__():
        pass
