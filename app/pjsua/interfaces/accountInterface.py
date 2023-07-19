from typing import Any, Mapping
import pjsua2 as pj
from pjsua.pjsua2exceptions.pjsua2AccountException import Pjsua2AccountException
from pjsua.pjsua2account import Pjsua2Account
from kivy.logger import Logger
from utils.config import load_to_instance
from collections import OrderedDict
from inspect import Parameter, Signature


class Descriptor:
    def __init__(self, *name):
        self.name = name

    def __get__(self, instance, cls):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        return

    def __delete__(self, instance):
        del instance.__dict__[self.name]
        return


import re


class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise ValueError("Length is Higher than ", self.maxlen)
        return super().__set__(instance, value)


class Regex(Descriptor):
    def __init__(self, *args, pat, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise ValueError("Value Doest Match With %s Pattern .%(self.pat)")
        return super().__set__(instance, value)


class Typed(Descriptor):
    ty = object

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise TypeError("Expected ", self.ty, "Got : ", type(value))
        return super().__set__(instance, value)


class Integer(Typed):
    ty = int


class String(Typed):
    ty = str


class Float(Typed):
    ty = float


class Positive(Descriptor):
    def __set__(self, instance, value):
        if not (value > 0):
            raise ValueError("Got Negative Integer ")
        return super().__set__(instance, value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class SizedString(String, Sized):
    pass


class SizedRegexString(SizedString, Regex):
    pass


def make_signature(args):
    return Signature([Parameter(i, Parameter.POSITIONAL_OR_KEYWORD) for i in args])


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

    def create_account_config(self, *args, **kwargs):
        """
        Creating the Pjsua2 Account Configration in this method.

        arguments:

        return:

        """
        try:
            print(self.name)
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

    def on_incomingcall(*args, **kwargs):
        print("INSIDE ONC_INCOMING CALLBACK FROM PJSUA" * 20)

    def on_register(*args, **kwargs):
        print("INSIDE ONMESSAGE")
