import pjsua2 as pj
from pjsua.pjsua2exceptions.pjsua2AccountException import Pjsua2AccountException
from pjsua.pjsua2account import Pjsua2Account
from typing import Dict, Any, Callable
from pjsua.common import (
    SizedRegexString,
    Integer,
    Descriptor,
    make_signature,
    load_to_instance,
)
from collections import OrderedDict
from collections.abc import Iterable


class Account(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, cls_dict):
        account = Pjsua2Account()
        cls_dict["account"] = account
        fields = [
            key for key, value in cls_dict.items() if isinstance(value, Descriptor)
        ]
        for key in fields:
            cls_dict[key].name = key

        cls_bdy = super().__new__(cls, name, bases, dict(cls_dict))
        bounded = make_signature(fields)
        setattr(cls_bdy, "__signature__", bounded)
        for k, value in cls_dict.items():
            if callable(value) and str(k).startswith("on"):
                for func_name, _ in account.callbacks.items():
                    if func_name == k:
                        account.callbacks.update({k: value})

        if not dict(cls_bdy.__dict__).get("name"):
            try:
                load_to_instance("config.yaml", cls_bdy)
            except (FileNotFoundError, FileExistsError) as e:
                print(e.args)

        return cls_bdy


class AccountStructure(metaclass=Account):
    """"""

    fields = []

    def __init__(self, *args, **kwargs) -> None:
        self.bind_signature(*args, **kwargs)

    def bind_signature(self, *args, **kwargs):
        bounded = self.__signature__.bind(*args, **kwargs)
        for attr_name, value in bounded.arguments.items():
            setattr(self, attr_name, value)


class AccountUtility(AccountStructure):
    """
    AccountUtlity Class consist of all the pjsuaAccount Utility function from Pjsua2.
    """

    """
    port: 0
    ip: 172.16.2.111
    name: 6002
    password: 1234
    
    """
    name = Integer()
    port = Integer()
    ip = SizedRegexString(maxlen=15, pat="")
    password = SizedRegexString(maxlen=50, pat="")

    def __init__(self, *args, callbacks: Dict[str, Callable], **kwargs) -> None:
        self._callbacks = callbacks
        super().__init__(*args, **kwargs)

    # def setcallback(self, callbacks: Dict[str, Callable]):
    #     """
    #     Appending All the Callback's with the previous callbacks
    #     """
    #     self.callbacks = {**self.callbacks, **callbacks}

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
            print(e)

    def create_account(self):
        try:
            self.account.create(
                self.acfg,
            )
        except Pjsua2AccountException as ace:
            print(ace.args)

    def on_incomingcall(self, *args, **kwargs):
        callback = self._callbacks.get("on_incomingcall")
        if isinstance(callback, Iterable):
            for func in callback:
                """
                When User Send's the callback function when creating the instance Dont need to pass the Param's inside the callback function's

                FIXME
                    In the Next Version in any other support we enchace the Library as More Efficient.
                """
                func()
        else:
            callback()

    def on_register(*args, **kwargs):
        """
        FIXME NEEDS TO ADD THE APPRAPRIATE CALLBACK ARGUMENTS OR PARAMETER
        Args:
        """
        print("INSIDE ONMESSAGE")

    def get_account(self):
        return self.account

    """
    Need's to Implement All the callback function and Utility Method for the Class.
    """
