import pjsua2 as pj


class Pjsua2Buddy(pj.Buddy):
    def print_pad(self, message, prefix="*") -> None:
        return print(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self):
        """
        Args:
            instance of the own class
        """
        super().__init__()

    def onBuddyState(self):
        super().onBuddyState()
        buddy_info: pj.BuddyInfo = self.getInfo()
        buddy_presence_status: pj.PresenceStatus = buddy_info.presStatus
        """
            Create the listener to handle all the state changes for buddy inside Buddy Utility.        
        """
        self.print_pad(f" Buddy State  ")
        self.print_pad(
            f"""
                    contact :: {buddy_info.contact}
                    presStatus :: {dir(buddy_presence_status)}
                    subStateName :: {buddy_info.subStateName}
                    subTermReason ::{buddy_info.subTermReason}
                    uri :: {buddy_info.uri}
                    subTermCode :: {buddy_info.subTermCode}
                    subState :: {buddy_info.subState}
                       """
        )
        self.print_pad("")

    def onBuddyEvSubState(self, param: pj.OnBuddyEvSubStateParam):
        """
        Create the listener to handle all the state changes for buddy inside Buddy Utility.
        """
        pass
