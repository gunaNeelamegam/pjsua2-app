import threading
from threading import Thread
from pjsua2 import Endpoint


class Pjsua2Thread(threading.Thread):
    """
    For handling the Pjsua2 Application in the Background Thread .
    This Class Mainly Handling the Pjsua2 in Background.
    """

    def __init__(self, endpoint: Endpoint = None):
        super().__init__()
        self.endpoint: Endpoint = endpoint
        self.stop_event: threading.Event = threading.Event()

    def set_endpoint(self, endpoint: Endpoint):
        if not self.endpoint:
            self.endpoint = endpoint

    def run(self):
        """
        When Calling the Start method Thread Start's the Pjsua2 Application.
        """
        self.endpoint.libRegisterThread("Pjsua2Thread")
        while not self.stop_event.is_set():
            if self.endpoint:
                self.endpoint.libHandleEvents(1)
        self.clean_up()

    def clean_up(self):
        """
        Clean-up method for deleting all the pjsua2 background tasks.
        """
        self.endpoint.libDestroy()

    def stop(self):
        """
        Stop method stop the processs when using with the Any Front-End Library.
        
        pros:
            with out using this method may or maynot crashes your application
        """
        self.stop_event.set()
