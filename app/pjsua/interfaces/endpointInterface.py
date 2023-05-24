import pjsua2 as pj
from pjsua.pjsua2endpoint import Pjsua2Endpoint
from kivy.logger import Logger
from utils.config import load_to_instance

class EndpointUtility:
    """
    EndpointUtility Class consist of all the utility methods in pjsuaEndpoint Class
    """

    def print_pad(message, prefix="*") -> None:
        return Logger.info(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self) -> None:
        load_to_instance("config.yaml",self)
        self.ep = Pjsua2Endpoint()
        self.ep_cfg: pj.EpConfig = pj.EpConfig()

    def init_endpoint(self):
        """
        method initalizing the endpoint one's inside application
        """

        log = pj.LogConfig()
        log.consoleLevel = 4
        log.level = 4

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
            self.ep.libStart()

        except Exception as e:
            self.print_pad(e.args)

    def get_all_codecs(self):
        codec: pj.CodecInfo
        for codec in self.ep.codecEnum2():
            print(f"{codec.codecId=} :: {codec.priority}")
        return self.ep.codecEnum2()

    def set_codec_priority(self, codec_id: str = "speex/32000/1", codec_priority=130):
        self.ep.codecSetPriority(codec_id, int(codec_priority))
