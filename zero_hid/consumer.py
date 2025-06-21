from .hid.consumer import send_consumer_event, send_consumer_event_identity
from . import defaults
from time import sleep
from typing import List
from collections import deque

class Consumer:

    def __init__(self, hid: Device):
        self.set_hid(hid)

    def tap(self, keys: List[int], delay=0):
        keys = deque(keys)

        keys_to_send = []

        # Send 1st to last key aggregated sequentially
        while len(keys) > 0:
            keys_to_send.append(keys.popleft())
            send_consumer_event(self.hid_file(), keys_to_send)
            print(f"send_consumer_event->keys:{keys_to_send}")

        # Send last to 1st key de-aggregated sequentially
        while len(keys_to_send) > 0:
            keys.append(keys_to_send.pop())
            send_consumer_event(self.hid_file(), keys_to_send)
            print(f"send_consumer_event->keys:{keys_to_send}")

        # Wait before next consumer key tap
        if delay > 0:
            sleep(delay)

    def press(self, keys: List[int], release=True):
        send_consumer_event(self.hid_file(), keys)
        if release:
            self.release()

    def release(self):
        send_consumer_event_identity(self.hid_file())

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()