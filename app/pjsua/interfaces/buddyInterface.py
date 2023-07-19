import pjsua2 as pj
from pjsua.pjsua2exceptions.pjsua2BuddyException import PjsuaBuddyException
from pjsua.pjsua2buddy import Pjsua2Buddy
from utils.config import load_to_instance
from pjsua.pjsua2account import Pjsua2Account
from typing import Dict, Any


class BuddyUtility:
    def __init__(self, account: Pjsua2Account) -> None:
        load_to_instance("config.yaml", self)
        self.account = account

    def create_buddy_config(self):
        """_summary_
        Create Buddy Configration.
        """
        buddy_config = pj.BuddyConfig()
        buddy_config.subscribe = True
        buddy_config.uri = f"sip:6001@{self.ip}"
        return buddy_config

    def create_buddy(self):
        """_summary_
        Create Buddy (or) Contacts based on your account.
        """
        self.buddy: pj.Buddy = Pjsua2Buddy()
        self.buddy.create(self.account, self.create_buddy_config())

    def send_text_message(self, options: Dict[str, Any]):
        """
        send message function's send to message to specify distination uri.
        Args:
            options (Dict[str,Any]): _description_
            options:
                attribute:
                message: str
                destination:str (destination uri)
                    Example: sip@guna@domain.com
            Note:
                Verify if the message sended successfully or not inside the listener callback function.
        """
        try:
            message_info: pj.SendInstantMessageParam = pj.SendInstantMessageParam()
            message_info.contentType = "text/plain"
            message_info.content = options.get("message")
            # message_info.userData = True
            self.buddy.sendInstantMessage(message_info)
            return True
        except Exception as e:
            print(*e.args)
            return False

    def send_typing(self):
        try:
            typing_indication: pj.SendTypingIndicationParam = (
                pj.SendTypingIndicationParam()
            )
            typing_indication.isTyping = True
            self.buddy.sendTypingIndication(typing_indication)
            return True
        except Exception as e:
            print(**e.args)
            return False
