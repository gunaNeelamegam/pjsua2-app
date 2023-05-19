import pjsua2 as pj
from main import pjapp


def print_pad(message, *, prefix="*"):
    return print(f"{prefix}\n\n{message}\n\n{prefix}")


class CallException(Exception):
    pass


class MyCall(pj.Call):
    """
    Call Class
    """

    PjAudioMedia: pj.AudioMedia = None
    PjMediaPreview: pj.VideoPreview = None
    PjVideoWindow: pj.VideoWindow = None
    PjVideoPreview: pj.VideoPreview = None

    def __init__(self, acc: pj.Account, call_id: int = ...):
        super().__init__(acc, call_id)

    def onCallState(self, prm: pj.OnCallStateParam):
        call_info: pj.CallInfo = pj.CallInfo()
        print_pad(
            f"Call Info : {call_info.callIdString} {call_info.stateText} {call_info}"
        )
        return super().onCallState(prm)

    def onCallMediaState(self, prm):
        super().onCallMediaState(prm)
        self.current_callmedia_state = pj.CallMediaInfo()
        call_info: pj.CallInfo = pj.CallInfo()
        self.current_call_info = call_info
        print_pad(f"{self.current_callmedia_state=}")
        if (
            self.current_callmedia_state.type == 1
            and self.current_callmedia_state.status == 3
        ):
            try:
                self.PjAudioMedia = self.current_call_info.media
                audio_manager = pjapp.ep.audDevManager()
                print_pad(f"{audio_manager=}")
            except Exception as e:
                print_pad(e)

    def __repr__(self) -> str:
        return super().__repr__()
