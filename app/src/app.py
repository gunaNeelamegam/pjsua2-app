"""
Main Application 

"""

import pjsua2 as pj
from utils.config import load_to_instance
from src.myaccount import Account


class AccountException(Exception):
    """
    Account Exception
    """


class App:

    """
    PJSUA2 APP
    """

    def print_pad(message, prefix="*") -> None:
        return print(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self, file_name: str = "config.yaml") -> None:
        """
        Initailzing the pjsua2 application.

        Make Sure:
            Endpoint must be create only ones in application.

        """
        load_to_instance(file_name, instance=self)
        self.init_endpoint()
        self.init_transport()
        self.set_accountconfig()
        self.create_account()
        """
        Must call only ones inside the entitre application context 
        """
        self.ep.libStart()

    def init_endpoint(self):
        """
        method initalizing the endpoint one's inside application
        """

        log = pj.LogConfig()
        log.consoleLevel = 4
        log.level = 4
        self.ep_cfg: pj.EpConfig = pj.EpConfig()
        self.ep = pj.Endpoint()
        try:
            self.ep.libCreate()
        except Exception as e:
            self.print_pad(e.args)
            return

        self.ua_config: pj.UaConfig = self.ep_cfg.uaConfig
        self.ua_config.threadCnt = 0
        self.ep.libInit(self.ep_cfg)

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
            self.acfg.natConfig.iceEnabled = True
            self.acfg.videoConfig.autoTransmitOutgoing = True
            self.acfg.videoConfig.autoShowIncoming = True
            self.acfg.mediaConfig.rtpUse = 1
            self.acfg.mediaConfig.srtpSecureSignaling = 0
            self.acfg.sipConfig.authCreds.append(self.cred)
        except Exception as e:
            self.print_pad(e)

    def create_account(self):
        try:
            self.acc: pj.Account = Account()
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
        call = pj.Call(self.acc)
        call.makeCall(f"sip:6002@{self.ip}")

    def __enter__():
        pass

    def __exit__():
        pass
