import pjsua2 as pj



class Account(pj.Account):
    
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason,prm)
    