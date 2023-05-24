"""
Main Controller for this Application 

"""

from kivy.logger import Logger
from pjsua.interfaces.endpointInterface import EndpointUtility
from pjsua.interfaces.accountInterface import AccountUtility
from pjsua.interfaces.callInterface import CallUtility
from pjsua.pjsua2endpoint import Pjsua2Endpoint


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
        self.ep_util = EndpointUtility()
        self.ep_util.init_endpoint()
        self.ep_util.init_transport()
        self.acc_util = AccountUtility()
        self.acc_util.create_account_config()
        self.acc_util.create_account()
        self.call_util = CallUtility(self.acc_util.account)

                

    def clean_up(self):
        """
        cleanup method:
            clean the pjsua2 memory

        """
        print(f"ENDPPOINT INSTANCE : {Pjsua2Endpoint.instance()}")
        Pjsua2Endpoint.instance().transportShutdown(self)
        self.acc_util.account.shutdown()
        Pjsua2Endpoint.instance().libDestroy()
        self.print_pad("Application Shutdown's", prefix="#")

    def __enter__():
        pass

    def __exit__():
        pass
