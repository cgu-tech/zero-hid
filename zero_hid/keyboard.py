from .hid.keyboard import send_keyboard_event, send_keyboard_event_identity, read_keyboard_state, LEDState, parse_leds, KEYBOARD_STATE_NONE
from .hid.keycodes import KeyCodes
from . import defaults
from time import sleep
import json
import pkgutil
import os
import pathlib
from typing import List
from collections import deque

class Keyboard:

    def __init__(self, hid: Device) -> None:
        self.set_hid(hid)
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

    def read_state(self) -> LEDState:
        state = read_keyboard_state(self.hid_file())

        # Return identity when state cannot be read
        if state is None:
            print("No LED data available (non-blocking).")
            state = KEYBOARD_STATE_NONE

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

                mods = deque(mods)
                keys = deque(keys)

                mods_to_send = []
                keys_to_send = []

                # Send 1st to last modifier aggregated sequentially
                while len(mods) > 0:
                    mods_to_send.append(mods.popleft())
                    send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
                    print(f"send_keyboard_event->mods:{mods_to_send},keys:{keys_to_send}")

                # Send all modifiers + 1st to last key aggregated sequentially
                while len(keys) > 0:
                    keys_to_send.append(keys.popleft())
                    send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
                    print(f"send_keyboard_event->mods:{mods_to_send},keys:{keys_to_send}")

                # Send all modifiers + last to 1st key de-aggregated sequentially
                while len(keys_to_send) > 0:
                    keys.append(keys_to_send.pop())
                    send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
                    print(f"send_keyboard_event->mods:{mods_to_send},keys:{keys_to_send}")

                # Send last to 1st modifier de-aggregated sequentially
                while len(mods_to_send) > 0:
                    mods.append(mods_to_send.pop())
                    send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
                    print(f"send_keyboard_event->mods:{mods_to_send},keys:{keys_to_send}")

            # Wait before next char type
            if delay > 0:
                sleep(delay)

    def press(self, mods: List[int], keys: List[int], release=True):
        send_keyboard_event(self.hid_file(), mods, keys)
        if release:
            self.release()

    def release(self):
        send_keyboard_event_identity(self.hid_file())

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()
