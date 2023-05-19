import threading
from kivy.app import App
from src.app import App as Pjsua2App
from threading import Thread
from pjsua2 import Endpoint


class Pjsua2Thread(threading.Thread):
    """
    For handling the Pjsua2 Application in the Background Thread .
    This Class Mainly Handling the Pjsua2 in Background.
    """

    def __init__(self, endpoint: Endpoint = None):
        super().__init__()
        self._endpoint: Endpoint = endpoint
        self.stop_event: threading.Event = threading.Event()

    def set_endpoint(self, endpoint: Endpoint):
        if not self._endpoint:
            self._endpoint = endpoint

    def run(self):
        """
        When Calling the Start method Thread Start's the Pjsua2 Application.
        """
        self._endpoint.libRegisterThread("Pjsua2Thread")
        while not self.stop_event.is_set():
            if self._endpoint:
                self._endpoint.libHandleEvents(1)
        self.clean_up()

    def clean_up(self):
        self._endpoint.libDestroy()

    def stop(self):
        self.stop_event.set()


class MyApp(App):

    """
    Initailzing the Main Kivy Application

    @params:
        pjsua2_thread: Thread Running the Pjsua2 in BackGround thread
        file_name:  config file path inside utils dir
    """

    def __init__(self, pjsua2_thread: Thread, file_name: str = ""):
        super().__init__()
        self.pjsua2_app = Pjsua2App()
        self.pjsua2_thread = pjsua2_thread

    def on_stop(self):
        """
        When Click Off the X-Cross Button it Automatically Stop the Pjsua2 Application.
        """
        self.pjsua2_thread.stop()
        self.pjsua2_thread.join()


if __name__ == "__main__":
    """
    Running the Pjsua2 Thread
    """
    pjsua2_thread = Pjsua2Thread()
    """
    Main Kivy App
    """
    my_app = MyApp(pjsua2_thread)
    endpoint: Endpoint = my_app.pjsua2_app.ep
    pjsua2_thread.set_endpoint(endpoint)
    pjsua2_thread.start()
    my_app.run()
