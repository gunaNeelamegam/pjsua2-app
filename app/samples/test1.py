import threading
import pjsua2
from kivy.app import App

class Pjsua2Thread(threading.Thread):
    def __init__(self, endpoint):
        super().__init__()
        self.endpoint = endpoint
        self.stop_event = threading.Event()

    def run(self):
        self.endpoint.libRegisterThread("Pjsua2Thread")
        while not self.stop_event.is_set():
            print(self.stop_event.is_set())
            self.endpoint.libHandleEvents(0.1)  # Adjust the timeout as needed
        self.endpoint.libUnregisterThread()

    def stop(self):
        self.stop_event.set()

class MyApp(App):
    def __init__(self, pjsua2_thread):
        super().__init__()
        self.pjsua2_thread = pjsua2_thread

    def on_stop(self):
        self.pjsua2_thread.stop()
        self.pjsua2_thread.join()


if __name__ == '__main__':
    # Create and initialize pjsua2 endpoint
    ep = pjsua2.Endpoint()
    ep_cfg = pjsua2.EpConfig()
    ep_cfg.logConfig.level = 4  # Set log level as needed
    ep.libCreate()
    ep.libInit(ep_cfg)

    # Create transport and configure account
    transport_config = pjsua2.TransportConfig()
    ep.transportCreate(pjsua2.PJSIP_TRANSPORT_UDP, transport_config)
    ep.libStart()

    # Create and configure account
    account_cfg = pjsua2.AccountConfig()
    # Set account configuration options
    # account = ep.createAccount(account_cfg)
    acfg: pjsua2.AccountConfig = pjsua2.AccountConfig()
    acfg.idUri = f"sip:6003@172.16.2.111"
    acfg.regConfig.registrarUri = f"sip:172.16.2.111"
    cred: pjsua2.AuthCredInfo = pjsua2.AuthCredInfo(
        "digest", "*", f"6003", 0, "1234"
    )
    acfg.natConfig.iceEnabled = True
    acfg.videoConfig.autoTransmitOutgoing = True
    acfg.videoConfig.autoShowIncoming = True
    acfg.mediaConfig.rtpUse = 1
    acfg.mediaConfig.srtpSecureSignaling = 0
    acfg.sipConfig.authCreds.append(cred)
    # account_config = pjsua2.AccountConfig()
    # account_config.idUri = "sip:6002@172.16.2.111"
    # account_config.regConfig.registrarUri = "sip:172.16.2.111"
    # account_config.sipConfig.authCreds.append(
    #     pjsua2.AuthCredInfo("digest", "*", "6003",0, "1234")
    # )
    account = pjsua2.Account()
    account.create(acfg)
    call = pjsua2.Call(account)

    # Start pjsua2 thread
    pjsua2_thread = Pjsua2Thread(ep)
    pjsua2_thread.start()

    # Start Kivy application
    MyApp(pjsua2_thread).run()

    # Clean up resources (if needed)
    ep.libDestroy()