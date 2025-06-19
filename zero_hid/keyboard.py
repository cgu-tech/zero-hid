from typing import List

from .hid.keyboard import send_keystroke, release_keys, read_last_report
from .hid.keycodes import KeyCodes
from . import defaults
from time import sleep
import json
import operator
from functools import reduce
import pkgutil
import os
import pathlib
from typing import TypedDict
from collections import deque

class LEDState(TypedDict):
    num_lock: bool
    caps_lock: bool
    scroll_lock: bool


class Keyboard:

    def __init__(self, dev=defaults.KEYBOARD_PATH) -> None:
        if not hasattr(dev, "write"):  # check if file like object
            self.dev = open(dev, "ab+")
        else:
            self.dev = dev
        self.set_layout()

    def list_layout(self):
        keymaps_dir = pathlib.Path(__file__).parent.absolute() / "keymaps"
        keymaps = os.listdir(keymaps_dir)
        files = [f for f in keymaps if f.endswith(".json")]
        for count, fname in enumerate(files, 1):
            with open(keymaps_dir / fname, encoding="UTF-8") as f:
                content = json.load(f)
                name, desc = content["Name"], content["Description"]
            print(f"{count}. {name}: {desc}")

    def blocking_read_led_status(self) -> LEDState:
        """
        **The function will block until the LED state has been read from the device.**
        """
        self.dev
        report = read_last_report(self.dev, 1)  # Read 1 byte from the HID device
        led_indicators = report[0]  # Convert the byte to an integer

        # Interpret the LED indicators
        return {
            "num_lock": (led_indicators & 0x01) != 0,
            "caps_lock": (led_indicators & 0x02) != 0,
            "scroll_lock": (led_indicators & 0x04) != 0,
        }

    def set_layout(self, language="US"):
        self.layout = json.loads(
            pkgutil.get_data(__name__, f"keymaps/{language}.json").decode()
        )

    def type(self, text, delay=0):
        for c in text:
            kb_map = self.layout["Mapping"][c]
            if kb_map is None:
                raise ValueError(f"No mapping found for character: {c}")

            # A single char may need one or multiple key combos
            for combo in kb_map:

                # Retrieve combo modifiers and keys names
                mods = combo["Modifiers"]
                keys = combo["Keys"]
                print(f"combo->mods:{mods},keys:{keys}")

                # Retrieve combo modifiers and keys codes
                mods = [KeyCodes[i] for i in mods]
                keys = [KeyCodes[i] for i in keys]

                # Send (1st)..(N-1th) keys + all modifiers
                keys = deque(keys)
                keys_to_send = []
                while len(keys) > 1:
                    keys_to_send.append(keys.popleft())
                    send_keyboard_event(self.dev, mods, keys_to_send)
                    print(f"send_keystroke->mods:{mods},keys:{keys_to_send}")

                # Send (Nth) key + all modifiers
                keys_to_send.append(keys.popleft() if len(keys) > 0 else 0)
                send_keyboard_event(self.dev, mods, keys_to_send)
                print(f"send_keystroke->mods:{mods},keys:{keys_to_send}")
                self.release()

            if delay > 0:
                sleep(delay)

    def press(self, modifiers: List[int], keys: List[int]: int = 0, release=True):
        send_keyboard_event(self.dev, modifiers, keys, release=release)
        if release:
            self.release()

    def release(self):
        send_keyboard_event_identity(self.dev)

    def __enter__(self):
        return self

    def _clean_resources(self):
        self.dev.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
