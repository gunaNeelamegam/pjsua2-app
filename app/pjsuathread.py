import threading
from threading import Thread
from pjsua2 import Endpoint


class Pjsua2Thread(threading.Thread):
    """
    For handling the Pjsua2 Application in the Background Thread .
    This Class Mainly Handling the Pjsua2 to invoke the Callback Frequntly by the  Background Thread.

    *If you want's to invoke the callback and Operation  subsequently must Need's to Register the External to Pjsua2 to invoke the Event.


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

        NOTE:

            self.endpoint.libHandleEvents(0.01)

            When Using this Api Only we can able to reveive the callback Event To process from the Register Thread.

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
