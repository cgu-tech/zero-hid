from . import defaults
import logging
import os
import time
logger = logging.getLogger(__name__)

class Device:

    def __init__(self, dev_path=defaults.HID_DEVICE_PATH) -> None:
        self.file = None
        self.open_file(dev_path)

    def open_file(self, dev_path):
        self._clean_resources()
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Opening HID device...")
            logger.debug(f"HID path: {dev_path}")
            logger.debug(f"HID path exists: {os.path.exists(dev_path)}")

        retries = 5
        for i in range(retries):
            if os.path.exists(dev_path):
                break
            time.sleep(0.2)
        else:
            raise RuntimeError(f"HID device never appeared: {dev_path}")

        try:
            self.dev_path = dev_path
            self.file = open(dev_path, "r+b")
        except Exception as ex:
            logger.exception(f"Unexpected error while opening HID device {self.dev_path}. error:{ex}")
            raise RuntimeError(f"HID device not available: {self.dev_path}") from ex

    def get_file(self):
        return self.file

    def __enter__(self):
        return self

    def _clean_resources(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Closing HID device...")
        try:
            if self.file:
                self.file.close()
                self.file = None
        except Exception as ex:
            logger.exception(f"Unexpected error while closing HID device {self.dev_path}. error:{ex}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
