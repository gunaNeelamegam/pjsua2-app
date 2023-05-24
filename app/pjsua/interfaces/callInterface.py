import pjsua2 as pj
from pjsua.pjsua2call import Pjsua2Call
from kivy.logger import Logger


class CallUtility:
    """
    CallUtility Handles all the call based method's

    """

    def print_pad(message, prefix="*") -> None:
        return Logger.info(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self, account: pj.Account = None) -> None:
        self.account = account

    def make_call(self):
        self.call = Pjsua2Call(self.account, 0)
        self.call.makeCall(f"sip:6001@{self.ip}", pj.CallOpParam(True))
