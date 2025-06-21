from . import defaults, Device
from .hid.consumer import send_consumer_event, send_consumer_event_identity
from collections import deque
from time import sleep
from typing import List
import logging
logger = logging.getLogger(__name__)

class Consumer:

    def __init__(self, hid: Device):
        self.set_hid(hid)

    def tap(self, keys: List[int], delay=0):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"keys:{keys},delay:{delay}")
        keys = deque(keys)

        keys_to_send = []

        logger.debug("Send 1st to last consumer key aggregated sequentially")
        while len(keys) > 0:
            keys_to_send.append(keys.popleft())
            send_consumer_event(self.hid_file(), keys_to_send)

        logger.debug("Send last to 1st consumer key de-aggregated sequentially")
        while len(keys_to_send) > 0:
            keys.append(keys_to_send.pop())
            send_consumer_event(self.hid_file(), keys_to_send)

        if delay > 0:
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(f"Wait {delay}s before next consumer key tap")
            sleep(delay)

    def press(self, keys: List[int], release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"keys:{keys},release={release}")
        send_consumer_event(self.hid_file(), keys)
        if release:
            self.release()

    def release(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Releasing...")
        send_consumer_event_identity(self.hid_file())

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()