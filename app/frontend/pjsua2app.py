from kivy.app import App
from threading import Thread
from pjsua import pjsua2controller
from pjsua2 import Endpoint
import os


from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label

from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):
    def __init__(self, **var_args):
        super(LoginScreen, self).__init__(**var_args)
        self.add_widget(Label(text="User Name"))
        self.username = TextInput(multiline=True)

        self.add_widget(self.username)
        self.add_widget(Label(text="password"))
        self.password = TextInput(password=True, multiline=False)

        self.add_widget(Label(text="Comfirm password"))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MyApp(App):
    cls_endpoint = None

    """
    Initailzing the Main Kivy Application

    @params:
        pjsua2_thread: Thread Running the Pjsua2 in BackGround thread
        file_name:  config file path inside utils dir
    """

    def __init__(self, pjsua2_thread: Thread, file_name: str = ""):
        self.pjsua2_app = pjsua2controller.PJSUA2Controller()
        self.pjsua2_thread = pjsua2_thread
        super.__init__()

    def build(self):
        print("inside Build")
        return LoginScreen()

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
        return Endpoint.instance()
