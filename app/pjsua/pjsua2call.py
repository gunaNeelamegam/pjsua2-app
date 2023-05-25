import pjsua2app
import pjsua2 as pj
from kivy.logger import Logger
import time
from pjsua.pjsua2endpoint import Pjsua2Endpoint


def print_pad(message, *, prefix="*"):
    return print(f" \n {prefix *20} \n {message}\n {prefix*20}")


class CallException(Exception):
    pass


class Pjsua2Call(pj.Call):
    """
    Call Class
    """

    def __init__(self, acc: pj.Account, call_id: int = ...):
        super(Pjsua2Call, self).__init__(acc, call_id)
        self.local_video = None
        self.remote_video = None
        self.start_time = time.time()
        self.end_time = None
        self.video_window = None
        self.video_prev = None

    def hangUp(self):
        param: pj.CallOpParam = pj.CallOpParam(True)
        param.statusCode = 603
        self.hangup(prm=param)

    def onCallState(self, prm: pj.OnCallStateParam):
        try:
            super(Pjsua2Call, self).onCallState(prm)
            callinfo: pj.CallInfo = self.getInfo()
            call_state = callinfo.state
            call_id = callinfo.id
            Logger.info(f"{'='*10} :: Call State :: {'='*10}")
            if call_state == pj.PJSIP_INV_STATE_CALLING:
                self.start_time = time.time()
            elif call_state in (
                pj.PJSIP_INV_STATE_DISCONNECTED,
                pj.PJSIP_INV_STATE_NULL,
            ):
                self.hangUp()
                self.end_time = time.time()
                duration = self.calculateDuration()
                Logger.info(
                    f"Call ID: {call_id}, Duration: {duration} seconds {duration/60}"
                )

            Logger.info(
                f"""
                       Call State :: \t {callinfo.state}
                       Call Status Text :: \t {callinfo.stateText}
                       Call Info  :: \t  {callinfo.remVideoCount}
                        """
            )

            Logger.info("=" * 50)
        except CallException as e:
            Logger.error(e.args)

    def calculateDuration(self):
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return int(duration)
        else:
            return 0

    def onCallMediaState(self, prm: pj.OnCallMediaStateParam):
        super().onCallMediaState(prm)
        call_info: pj.CallInfo = self.getInfo()
        media: pj.CallMediaInfoVector = call_info.media
        media_count = media.size()
        print_pad(f"{call_info.totalDuration=}")
        for i in range(media_count):
            media_info: pj.CallMediaInfo = call_info.media[i]
            print_pad(f" {i=}")
            media_index = media_info.index
            media_type = media_info.type
            media_direction = media_info.dir
            active = media_info.dir == pj.PJSUA_CALL_MEDIA_ACTIVE

            if media_type == pj.PJMEDIA_TYPE_AUDIO:
                try:
                    self.audio_media: pj.AudioMedia = self.getAudioMedia(
                        med_idx=media_index
                    )
                    self.audio_media_manager: pj.AudDevManager = (
                        pjsua2app.MyApp.cls_endpoint.audDevManager()
                    )

                    self.audio_media_manager.getCaptureDevMedia().startTransmit(
                        self.audio_media
                    )

                    self.audio_media.startTransmit(
                        pjsua2app.MyApp.cls_endpoint.audDevManager().getPlaybackDevMedia()
                    )
                except Exception as e:
                    Logger.error(e.args)
            if media_type == pj.PJMEDIA_TYPE_VIDEO:
                try:
                    """
                    media_.videoIncomingWindowId
                    media_.audioConfSlot
                    media_.dir
                    media_.index
                    media_.status
                    media_.type
                    media_.videoCapDev
                    media_.videoWindow"""
                    # print_pad(
                    #     f"{dir(media_info.videoWindow)} :: {media_info.audioConfSlot=} :: {media_info.videoIncomingWindowId=}:: {media_info.videoCapDev=} {media_info.type=} :: { media_info.index=}"
                    # )
                    try:
                        video_wid: pj.VideoWindow = pj.VideoWindow(
                            media_info.videoIncomingWindowId
                        )
                        video_pre: pj.VideoPreview = pj.VideoPreview(
                            media_info.videoCapDev
                        )
                        param: pj.VideoPreviewOpParam = pj.VideoPreviewOpParam()
                        video_wid.Show(True)
                        video_pre.start(param)

                    except Exception as e:
                        print_pad(f"Exception At {e.args}")
                except Exception as e:
                    Logger.error(e.args)

    def startVideoTransfer(self):
        if self.local_video and self.remote_video:
            self.vidSetStream(self.local_video, 0)
            self.vidSetStream(self.remote_video, 1)
            self.vidStartTransmit(self.remote_video)

    def stopVideoTransfer(self):
        if self.local_video and self.remote_video:
            self.vidStopTransmit(self.remote_video)
            self.vidSetStream(None, 0)
            self.vidSetStream(None, 1)
            self.local_video = None
            self.remote_video = None

    def __repr__(self) -> str:
        super(Pjsua2Call, self).__repr__()

    def onDtmfDigit(self, digits):
        super(Pjsua2Call, self).onDtmfDigit(digits)
        print("DTMF Digit:", digits)

    def onCallTransferRequest(self, dstUri, referTo, options):
        super(Pjsua2Call, self).onCallTransferRequest(dstUri, referTo, options)
        print("Transfer Requested")
        # Implement transfer logic here

    def onCallTransferStatus(self, code, reason, final):
        print("Transfer Status:", code, reason, final)
        # Handle transfer status

    def onCallReplaceRequest(self, newCall):
        print("Call Replace Requested")
        # Implement call replace logic here

    def onCallReplaced(self, newCall):
        print("Call Replaced")
        # Handle call replaced event

    def onCallSdpCreated(self, sdp, len):
        print("Call SDP Created", sdp, len)
        # Handle SDP creation event

    def onCallSdpChanged(self):
        print("Call SDP Changed")
        # Handle SDP change event

    def onInstantMessage(self, mimeType, body):
        print("Instant Message:", mimeType, body)
        # Handle instant message received

    def onInstantMessageStatus(self, body, reason, code):
        print("Instant Message Status:", body, reason, code)
        # Handle instant message status

    def onTypingIndication(self, indication):
        print("Typing Indication:", indication)
        # Handle typing indication

    def onCallMediaTransportState(self, state):
        print("Call Media Transport State:", state)
        # Handle media transport state

    def onStreamCreated(self, strm):
        print("Stream Created")
        # Handle stream creation event

    def onStreamDestroyed(self, strm):
        print("Stream Destroyed")
        # Handle stream destruction event

    def onStreamStarted(self, strm):
        print("Stream Started")
        # Handle stream start event

    def onStreamStopped(self, strm):
        print("Stream Stopped")
        # Handle stream stop event

    def onStreamRead(self, strm, buf):
        print("Stream Read")
        # Handle stream read event

    def onStreamWrite(self, strm, buf):
        print("Stream Write")
        # Handle stream write event

    def onStreamOverflow(self, strm):
        print("Stream Overflow")
        # Handle stream overflow event

    def onStreamUnderflow(self, strm):
        print("Stream Underflow")
        # Handle stream underflow event

    def onStreamException(self, strm):
        print("Stream Exception")
        # Handle stream exception event

    def onCallMediaEvent(self, event):
        print("Call Media Event")
        # Handle call media event

    def onCallRedirected(self, targetUri):
        print("Call Redirected")
        # Handle call redirected event

    def onCallTransferRequest2(self, srcCall, referTo, options):
        print("Transfer Requested (Version 2)")
        # Implement transfer logic here

    def onCallTransferStatus2(self, code, reason, final, srcCall):
        print("Transfer Status (Version 2):", code, reason, final)
        # Handle transfer status (Version 2)

    def onCallRxOffer(self, prm):
        print("Call Rx Offer")
        # Handle incoming call offer

    def onCallTxOffer(self, prm):
        print("Call Tx Offer")
        # Handle outgoing call offer

    def onCallRxReinvite(self, prm):
        print("Call Rx Reinvite")
        # Handle incoming reinvite

    def onCallRxReinviteResponse(self, prm):
        print("Call Rx Reinvite Response")
        # Handle incoming reinvite response

    def onCallTxReinviteResponse(self, prm):
        print("Call Tx Reinvite Response")
        # Handle outgoing reinvite response

    def onCallTransferRequest(self, dstUri, referTo, options):
        print("Call Transfer Request")
        # Handle transfer request

    def onCallTransferStatus(self, code, reason, final):
        print("Call Transfer Status")
        # Handle transfer status

    def onCallMediaTransportState(self, state):
        print("Call Media Transport State")
        # Handle media transport state

    def onCallMediaEvent(self, event):
        print("Call Media Event")
        # Handle call media event


"""

Before Video Preview

# endpoint: pj.Endpoint = Pjsua2Endpoint.instance()
                        # video_dev_manager: pj.VidDevManager = endpoint.vidDevManager()
                        # param: pj.VideoPreviewOpParam = pj.VideoPreviewOpParam()
                        # preview: pj.VideoPreview = pj.VideoPreview(media_index)
                        # preview.start(param)
                        # window: pj.VideoWindow = preview.getVideoWindow()
                        # window_info: pj.VideoWindowInfo = window.getInfo()
                        # # print(window.getVideoMedia(),"%"*20)
                        # window.Show(True)

"""
