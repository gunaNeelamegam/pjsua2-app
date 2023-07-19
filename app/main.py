from pjsuathread import Pjsua2Thread
from pjsua2 import Endpoint
import pjsua2app
from threading import Thread

if __name__ == "__main__":
    pjsua2_thread: Thread = Pjsua2Thread()
    my_app = pjsua2app.MyApp(pjsua2_thread)
    endpoint: Endpoint = my_app.get_endpoint()
    pjsua2_thread.set_endpoint(endpoint)
    pjsua2app.MyApp.set_class_endpoint(endpoint)
    pjsua2_thread.start()
    my_app.run()
