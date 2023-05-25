from kivy.app import App
from threading import Thread
from pjsua import pjsua2controller
from pjsua2 import Endpoint

class MyApp(App):
    cls_endpoint = None

    """
    Initailzing the Main Kivy Application

    @params:
        pjsua2_thread: Thread Running the Pjsua2 in BackGround thread
        file_name:  config file path inside utils dir
    """

    def __init__(self, pjsua2_thread: Thread, file_name: str = ""):
        super(MyApp, self).__init__()
        self.pjsua2_app = pjsua2controller.PJSUA2Controller()
        self.pjsua2_thread = pjsua2_thread

    def on_stop(self):
        """
        When Click Off the X-Cross Button it Automatically Stop the Pjsua2 Application.
        """
        self.pjsua2_thread.stop()
        self.pjsua2_thread.join()

    @classmethod
    def set_class_endpoint(cls, cls_end) -> None:
        cls.cls_endpoint = cls_end
        print(f"{cls.cls_endpoint=}")
        return None

    def get_endpoint(self) -> Endpoint:
        return self.pjsua2_app.ep_util.ep
