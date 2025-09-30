from . import defaults
import alsaaudio
import asyncio
import threading
import logging
logger = logging.getLogger(__name__)

class Microphone:

    def __init__(self, out_card=defaults.AUX_OUTPUT_DEVICE) -> None:
        self.set_output_card(out_card)
        self._lock = threading.Lock()  # Prevent race conditions

    def set_output_card(self, out_card: str) -> None:
        self.out_card = out_card

    def start_audio(self) -> None:
        if self.output_device is None:
            output_device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, self.out_card)
            output_device.setchannels(1)
            output_device.setrate(16000)
            output_device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
            self.output_device = output_device

    def write_audio(self, buf) -> None:
        length = len(buf)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Microphone.write_audio(buf) -> length: {length}")
        with self._lock:
            try:
                if length > 0:
                    self.start_audio()
                    self.output_device.write(buf)
            except alsaaudio.ALSAAudioError as e:
                self.stop_audio()
                logger.exception(f"Unhandled error in Microphone.write_audio: {e}")

    def stop_audio(self) -> None:
        self.output_device = None