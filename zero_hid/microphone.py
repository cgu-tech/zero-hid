from . import defaults
import alsaaudio
import logging
logger = logging.getLogger(__name__)

class Microphone:

    def __init__(self, out_card=defaults.AUX_OUTPUT_DEVICE) -> None:
        self.set_output_device(out_card)

    def set_output_device(self, out_card: str) -> None:
        format = alsaaudio.PCM_FORMAT_S16_LE
        channels = 1
        rate = 16000
        periodsize = 128
        output_device = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, out_card)
        output_device.setchannels(channels)
        output_device.setrate(rate)
        output_device.setformat(format)
        output_device.setperiodsize(periodsize)
        self.output_device = output_device

    def write_audio(self, buf) -> None:
        length = len(buf)
        if _LOGGER.getEffectiveLevel() == logging.DEBUG:
            _LOGGER.debug(f"Microphone.write_audio(buf) -> length: {length}")
        try:
            if length > 0:
                self.output_device.write(buf)
        except alsaaudio.ALSAAudioError as e:
            _LOGGER.exception(f"Unhandled error in Microphone.write_audio: {e}")
