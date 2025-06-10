# zero_hid/consumer.py

from .hid.consumer import send_keystroke, release_keys
from . import defaults
from time import sleep

class Consumer:
    """
    High-level API for sending Consumer HID events.
    """

    def __init__(self, dev=defaults.CONSUMER_PATH):
        if not hasattr(dev, "write"):  # check if file-like object
            self.dev = open(dev, "ab+")
        else:
            self.dev = dev

    def press(self, key_code: int = 0, release=True):
        send_keystroke(self.dev, key_code, release=release)

    def release(self):
        release_keys(self.dev)

    def tap(self, key_code, delay=0):
        send_keystroke(self.dev, key_code, release=False)
        sleep(delay)
        release_keys(self.dev)

    def _clean_resources(self):
        if self.dev:
            self.dev.close()
            self.dev = None

    def close(self):
        self._clean_resources()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()
