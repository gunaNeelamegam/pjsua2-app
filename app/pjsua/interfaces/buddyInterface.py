import pjsua2 as pj
from pjsua.pjsua2exceptions.pjsua2BuddyException import PjsuaBuddyException
from pjsua.pjsua2buddy import Pjsua2Buddy
from utils.config import load_to_instance


class BuddyUtility:
    def __init__(self, account: pj.Account) -> None:
        load_to_instance("config.yaml", self)
        self.account = account

    def create_buddy_config(self):
        """_summary_
        Create Buddy Configration.
        """
        buddy_config = pj.BuddyConfig()
        buddy_config.subscribe(True)
        buddy_config.uri = f"sip:6003@{self.ip}"

    def create_buddy(self):
        """_summary_
        Create Buddy (or) Contacts based on your account.
        """
        self.buddy: pj.Buddy = Pjsua2Buddy()
        self.buddy.create(self.account, self.create_buddy_config())
