from . import defaults
import logging
logger = logging.getLogger(__name__)

class Device:

    def __init__(self, dev_path=defaults.HID_DEVICE_PATH) -> None:
        self.file = None
        self.open_file(dev_path)

    def open_file(self, dev_path):
        self._clean_resources()
        self.dev_path = dev_path
        try:
            self.file = open(dev_path, "r+b")
        except Exception as e:
            logger.exception(f"Unexpected error while opening device {self.dev_path}. error:{e}")

    def get_file(self):
        return self.file

    def __enter__(self):
        return self

    def _clean_resources(self):
        try:
            if self.file:
                self.file.close()
                self.file = None
        except Exception as e:
            logger.exception(f"Unexpected error while closing device {self.dev_path}. error:{e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
