import pjsua2 as pj
from pjsua.pjsua2call import Pjsua2Call
from kivy.logger import Logger
from pjsua.pjsua2endpoint import Pjsua2Endpoint
from pjsua.pjsua2account import Pjsua2Account
from pjsua.pjsua2exceptions.pjsua2CallException import PjsuaCallException
from utils.config import load_to_instance
import time


class CallUtility:
    """
    CallUtility Handles all the call based method's

    """

    def print_pad(self, message, prefix="*") -> None:
        return Logger.info(f"{prefix*50} \n \n{message}\n \n {prefix*50}")

    def __init__(self, account: pj.Account = None) -> None:
        load_to_instance("config.yaml", self)
        self.account = account

    def mute_call(self, state: str):
        """_summary_
        Mute the pjsua2 Call
        """
        try:
            if self.call:
                self.print_pad(" :: self call  ::")
                self.call.audio_media.adjustRxLevel(0)
                self.print_pad(f" :: Call Muted :: ")
            elif Pjsua2Account.incoming_call:
                print(f" :: Incoming Call :: ")
                Pjsua2Account.incoming_call.audio_media.adjustRxLevel(0)
                self.print_pad(f":: Call Muted ::")
        except PjsuaCallException as e:
            self.print_pad(e.args)

    def make_call(self):
        try:
            self.call = Pjsua2Call(self.account, 0)
            self.call.makeCall(f"sip:6001@{self.ip}", pj.CallOpParam(True))
        except PjsuaCallException as e:
            self.print_pad(f":: {e.args} :: ")

    def unmute_call(self):
        try:
            if self.call:
                self.print_pad(" :: self call  ::")
                self.call.audio_media.adjustRxLevel(1)
                self.print_pad(f" :: call unmuted :: ")
            elif Pjsua2Account.incoming_call:
                print(f" :: incoming call :: ")
                Pjsua2Account.incoming_call.audio_media.adjustRxLevel(1)
                self.print_pad(f":: call muted ::")
        except PjsuaCallException as e:
            self.print_pad(e.args)

    def hold_call(self):
        try:
            if self.call:
                prm: pj.CallOpParam = pj.CallOpParam(True)
                prm.statusCode = pj.PJSUA_CALL_UPDATE_CONTACT
                prm.reason = "hold"
                self.call.setHold(prm)
            elif Pjsua2Account.incoming_call:
                prm: pj.CallOpParam = pj.CallOpParam(True)
                prm.statusCode = pj.PJSUA_CALL_UPDATE_CONTACT
                prm.reason = "hold"
                Pjsua2Account.incoming_call.setHold(prm)
        except PjsuaCallException as e:
            self.print_pad(e.args)

    def unhold_call(self):
        try:
            if self.call:
                prm: pj.CallOpParam = pj.CallOpParam(True)
                prm.statusCode = pj.PJSUA_CALL_UPDATE_CONTACT
                prm.reason = "unhold"
                prm.opt.flag = 1
                self.call.reinvite(prm)
            elif Pjsua2Account.incoming_call:
                prm: pj.CallOpParam = pj.CallOpParam(True)
                prm.statusCode = pj.PJSUA_CALL_UPDATE_CONTACT
                prm.reason = "unhold"
                prm.opt.flag = 1
                Pjsua2Account.incoming_call.reinvite(prm)
        except PjsuaCallException as e:
            self.print_pad(e.args)

    def videoCall(self):
        try:
            prm: pj.CallOpParam = pj.CallOpParam(True)
            prm.opt.videoCount = 1
            prm.opt.audioCount = 1
            self.call = Pjsua2Call(self.account, 0)
            self.call.makeCall(f"sip:6001@{self.ip}", prm=prm)
        except PjsuaCallException as e:
            self.print_pad(f":: {e.args} :: ")

    def audio_call(self, callee: str = "sip6001@{self.ip}"):
        try:
            prm: pj.CallOpParam = pj.CallOpParam(True)
            self.call = Pjsua2Call(self.account, 0)
            self.call.makeCall(f"sip:6001@{self.ip}", prm=prm)
        except PjsuaCallException as e:
            self.print_pad(f":: {e.args} :: ")

    def transfer_call(
        self,
        transfer_uri: str,
    ):
        try:
            prm: pj.CallOpParam = pj.CallOpParam(True)
            self.call.xfer(transfer_uri, prm)
        except PjsuaCallException as e:
            self.print_pad(f":: {e.args} :: ")

    def play_ringtone(self, file_name: str):
        """
        Play Ringtone method is used for playing the audio file.

        Args:
            file_name (str): filename for audio file to play.
        """
        endpoint: pj.Endpoint = MyApp.cls_endpoint
        audio_dev_manager: pj.AudDevManager = endpoint.audDevManager()
        self.play_back_dev = audio_dev_manager.getPlaybackDevMedia()

        self.audio_player = pj.AudioMediaPlayer()
        self.audio_player.createPlayer(file_name)
        self.audio_player.startTransmit(self.play_back_dev)

    def stop_ringtone(self):
        """
        stop_ringtone method is used for stop the audio player.
        Args:

        """
        if self.audio_player and self.play_back_dev:
            self.audio_player.stopTransmit(self.play_back_dev)
            del self.play_back_dev
            del self.audio_player

    def start_recording(self, state="call", file_name: str = "recorder.wav"):
        """_summary_

        Args:
            state (str): describe when you needed.
                example: state=call state=record
            file_name (str): _description_
        """
        self.wav_writer: pj.AudioMediaRecorder = pj.AudioMediaRecorder()
        self.mic_media: pj.AudioMedia = (
            Pjsua2Endpoint.instance().audDevManager().getCaptureDevMedia()
        )
        try:
            self.wav_writer.createRecorder(f"{time.time()}.wav")
            self.mic_media.startTransmit(self.wav_writer)
        except Exception as e:
            self.mic_media.stopTransmit(self.wav_writer)
            del self.wav_writer
            del self.mic_media
            self.print_pad(e.args)

    def stop_recording(self):
        """_summary_"""
        try:
            if self.wav_writer and self.mic_media:
                self.mic_media.stopTransmit(self.wav_writer)
                del self.wav_writer
                del self.mic_media
                delattr(self, "wav_writer")
                delattr(self, "mic_media")
        except Exception as e:
            self.print_pad(e.args)
