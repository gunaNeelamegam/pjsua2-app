import pjsua2 as pj
from pjsua.pjsua2exceptions.pjsua2AccountException import Pjsua2AccountException
from pjsua.pjsua2account import Pjsua2Account
from kivy.logger import Logger
from utils.config import load_to_instance


class AccountUtility:
    """
    AccountUtlity Class consist of all the pjsuaAccount Utility function from Pjsua2.
    """

    def __init__(self) -> None:
        """
        As of now we load all the default settings from yaml file as config.yaml inside config directory.
        """

        load_to_instance("config.yaml", self)
        self.account: pj.Account = Pjsua2Account()

    def create_account_config(self, *args, **kwargs):
        """
        Creating the Pjsua2 Account Configration in this method.

        arguments:

        return:

        """
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
            self.account.create(
                self.acfg,
            )
        except Pjsua2AccountException as ace:
            self.print_pad(ace.args)

    def print_pad(message, prefix="*") -> None:
        return Logger.info(f"{prefix*50} \n \n{message}\n \n {prefix*50}")
