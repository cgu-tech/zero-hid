from . import defaults
import logging
import os
import time
logger = logging.getLogger(__name__)

class Device:

    def __init__(self, dev_path=defaults.HID_DEVICE_PATH) -> None:
        self.dev_path = dev_path
        self._fd = None
        self.reopen()

    def get_file_descriptor(self):
        return self._fd

    def reopen(self):
        self._clean_resources()
        try:
            self._wait_for_device()
            self._open()
        except Exception as ex:
            raise RuntimeError(f"Unexpected error while reseting HID device {self.dev_path}. error:{ex}") from ex

    def _wait_for_device(self):
        # Total wait = retries x wait_per_retry
        retries = 5
        wait_per_retry = 0.2

        # Total wait for 1 second
        for _ in range(retries):
            if os.path.exists(self.dev_path):
                break
            time.sleep(wait_per_retry)
        else:
            raise RuntimeError(f"HID device never appeared: {self.dev_path}")

    def _open(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Opening HID device...")
            logger.debug(f"HID path: {self.dev_path}")
            logger.debug(f"HID path exists: {os.path.exists(self.dev_path)}")
        try:
            self._fd = open(self.dev_path, "r+b")
        except Exception as ex:
            raise RuntimeError(f"Unexpected error while opening HID device {self.dev_path}. error:{ex}") from ex

    def __enter__(self):
        return self

    def _clean_resources(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Closing HID device...")
        try:
            if self._fd:
                self._fd.close()
                self._fd = None
        except Exception as ex:
            logger.warning(f"Unexpected error while closing HID device {self.dev_path}. error:{ex}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
