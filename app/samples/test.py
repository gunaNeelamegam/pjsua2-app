import threading
import kivy

kivy.require("2.0.0")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import pjsua2


# Custom pjsua2 thread class
class Pjsua2Thread(threading.Thread):
    def run(self):
        # Create pjsua2 endpoint and initialize
        ep = pjsua2.Endpoint()
        ep.libCreate()

        # Configure endpoint and transport
        epconf = pjsua2.EpConfig()
        epconf.uaConfig.threadCount = 0
        ep.libInit(epconf)
        transport_config = pjsua2.TransportConfig()
        ep.transportCreate(pjsua2.PJSIP_TRANSPORT_UDP, transport_config)
        ep.libStart()

        # Create and configure account
        self.acfg: pjsua2.AccountConfig = pjsua2.AccountConfig()
        self.acfg.idUri = f"sip:6001@172.16.2.111"
        self.acfg.regConfig.registrarUri = f"sip:172.16.2.111"
        self.cred: pjsua2.AuthCredInfo = pjsua2.AuthCredInfo(
            "digest", "*", f"6001", 0, "1234"
        )
        self.acfg.natConfig.iceEnabled = True
        self.acfg.videoConfig.autoTransmitOutgoing = True
        self.acfg.videoConfig.autoShowIncoming = True
        self.acfg.mediaConfig.rtpUse = 1
        self.acfg.mediaConfig.srtpSecureSignaling = 0
        self.acfg.sipConfig.authCreds.append(self.cred)
        # account_config = pjsua2.AccountConfig()
        # account_config.idUri = "sip:6002@172.16.2.111"
        # account_config.regConfig.registrarUri = "sip:172.16.2.111"
        # account_config.sipConfig.authCreds.append(
        #     pjsua2.AuthCredInfo("digest", "*", "6003",0, "1234")
        # )
        account = pjsua2.Account()
        account.create(self.acfg)
        call = pjsua2.Call(account)
        # Make an outgoing call
        def make_call(d):
            # call = account.createCall("sip:destination@domain.com")
            call.makeCall("sip:6001@172.16.2.111",pjsua2.CallOpParam())

        # Schedule call after 5 seconds
        Clock.schedule_once(make_call,5)

        # Run the pjsua2 event loop
        # ep.libHandleEvents(100)
        
        print("After ".upper())
        # Clean up resources
        ep.libDestroy()


# Custom Kivy app
class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=50)
        label = Label(text="Kivy App")
        button = Button(text="Click Me")
        pjsua2_thread = Pjsua2Thread()
        pjsua2_thread.setName("name")
        pjsua2_thread.start()

        layout.add_widget(label)
        layout.add_widget(button)
        return layout


if __name__ == "__main__":
    # Start pjsua2 thread
    

    # Run Kivy app
    MyApp().run()

    # Terminate pjsua2 thread
