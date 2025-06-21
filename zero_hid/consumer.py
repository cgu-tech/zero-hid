from .hid.consumer import send_consumer_event, send_consumer_event_identity
from . import defaults
from time import sleep
from typing import List
from collections import deque

class Consumer:

    def __init__(self, dev=defaults.CONSUMER_PATH):
        if not hasattr(dev, "write"):  # check if file-like object
            self.dev = open(dev, "r+b")
        else:
            self.dev = dev

    def tap(self, keys: List[int], delay=0):
        keys = deque(keys)

        keys_to_send = []

        # Send 1st to last key aggregated sequentially
        while len(keys) > 0:
            keys_to_send.append(keys.popleft())
            send_consumer_event(self.dev, keys_to_send)
            print(f"send_consumer_event->keys:{keys_to_send}")

        # Send last to 1st key de-aggregated sequentially
        while len(keys_to_send) > 0:
            keys.append(keys_to_send.pop())
            send_consumer_event(self.dev, keys_to_send)
            print(f"send_consumer_event->keys:{keys_to_send}")

        # Wait before next consumer key tap
        if delay > 0:
            sleep(delay)

    def press(self, keys: List[int], release=True):
        send_consumer_event(self.dev, keys)
        if release:
            self.release()

    def release(self):
        send_consumer_event_identity(self.dev)

    def __enter__(self):
        return self

    def _clean_resources(self):
        if self.dev:
            self.dev.close()
            self.dev = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
