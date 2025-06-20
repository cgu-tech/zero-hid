from typing import List

from .hid.keyboard import send_keyboard_event, send_keyboard_event_identity, read_last_report
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
    compose: bool
    kana: bool

class Keyboard:

    def __init__(self, dev=defaults.KEYBOARD_PATH) -> None:
        if not hasattr(dev, "write"):  # check if file like object
            self.dev = open(dev, "r+b")
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

    def parse_leds(leds: int) -> LEDState:
        """
        Parse the 5-bit LED state integer into a dictionary of boolean LED states.
        
        :param leds: int with bits for LEDs (0b000xxxxx)
        :return: LEDState dict
        """
        return LEDState(
            num_lock=bool(leds & 0b00001),     # bit 0
            caps_lock=bool(leds & 0b00010),    # bit 1
            scroll_lock=bool(leds & 0b00100),  # bit 2
            compose=bool(leds & 0b01000),      # bit 3
            kana=bool(leds & 0b10000),         # bit 4
        )

    def read_state(self) -> LEDState:
        """
        **The function will block until the LED state has been read from the device.**
        """
        state = read_keyboard_state(self.dev)

        # Return identity when state cannot be read
        if state is None:
            print("No LED data available (non-blocking).")
            state = 0b00000

        leds = self.parse_leds(state)
        return leds

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

                # Retrieve combo mods and keys names
                mods = combo["Modifiers"]
                keys = combo["Keys"]
                print(f"combo->mods:{mods},keys:{keys}")

                # Retrieve combo modifiers and keys codes
                mods = [KeyCodes[i] for i in mods]
                keys = [KeyCodes[i] for i in keys]

                # Send (1st)..(N-1th) keys + all modifiers
                keys = deque(keys)
                keys_to_send = []
                while len(keys) > 0:
                    keys_to_send.append(keys.popleft())
                    send_keyboard_event(self.dev, mods, keys_to_send)
                    print(f"send_keyboard_event->mods:{mods},keys:{keys_to_send}")

                self.release()
                print(f"released->mods:{mods},keys:{keys_to_send}")              

            if delay > 0:
                sleep(delay)

    def press(self, mods: List[int], keys: List[int], release=True):
        send_keyboard_event(self.dev, mods, keys)
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
