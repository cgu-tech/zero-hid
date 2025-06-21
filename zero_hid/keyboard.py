from . import defaults, Device
from .hid.keyboard import send_keyboard_event, send_keyboard_event_identity, read_keyboard_state, LEDState, parse_leds, KEYBOARD_STATE_NONE
from .hid.keycodes import KeyCodes
from collections import deque
from time import sleep
from typing import List
import json
import pkgutil
import os
import pathlib
import logging
logger = logging.getLogger(__name__)


class Keyboard:

    def __init__(self, hid: Device, language="US") -> None:
        self.set_hid(hid)
        self.set_layout(language)

    def list_layout(self):
        keymaps_dir = pathlib.Path(__file__).parent.absolute() / "keymaps"
        keymaps = os.listdir(keymaps_dir)
        files = [f for f in keymaps if f.endswith(".json")]
        for count, fname in enumerate(files, 1):
            with open(keymaps_dir / fname, encoding="UTF-8") as f:
                content = json.load(f)
                name, desc = content["Name"], content["Description"]
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(f"{count}. {name}: {desc}")

    def read_state(self) -> LEDState:
        state = read_keyboard_state(self.hid_file())

        # Return identity when state cannot be read
        if state is None:
            logger.warning("No LED data available")
            state = KEYBOARD_STATE_NONE

        leds = self.parse_leds(state)
        return leds

    def set_layout(self, language):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"language:{language}")
        self.language = language
        self.layout = json.loads(
            pkgutil.get_data(__name__, f"keymaps/{language}.json").decode()
        )

    def type(self, text, delay=0):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"text:{text},delay:{delay}")
        if text:
            for c in text:
                if logger.getEffectiveLevel() == logging.DEBUG:
                    logger.debug(f"c:{c}")
                kb_map = self.layout["Mapping"][c]
                if kb_map is None:
                    raise ValueError(f"No mapping found for character: {c}")
            
                # A single char may need one or multiple key combos
                for combo in kb_map:
            
                    # Retrieve combo mods and keys names
                    mods = combo["Modifiers"]
                    keys = combo["Keys"]
                    if logger.getEffectiveLevel() == logging.DEBUG:
                        logger.debug(f"c:{c} combo->mods:{mods},keys:{keys}")
            
                    # Retrieve combo modifiers and keys codes
                    mods = [KeyCodes[i] for i in mods]
                    keys = [KeyCodes[i] for i in keys]
            
                    mods = deque(mods)
                    keys = deque(keys)
            
                    mods_to_send = []
                    keys_to_send = []
            
                    logger.debug("Send 1st to last modifier aggregated sequentially")
                    while len(mods) > 0:
                        mods_to_send.append(mods.popleft())
                        send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
            
                    logger.debug("Send all modifiers + 1st to last key aggregated sequentially")
                    while len(keys) > 0:
                        keys_to_send.append(keys.popleft())
                        send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
            
                    logger.debug("Send all modifiers + last to 1st key de-aggregated sequentially")
                    while len(keys_to_send) > 0:
                        keys.append(keys_to_send.pop())
                        send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
            
                    logger.debug("Send last to 1st modifier de-aggregated sequentially")
                    while len(mods_to_send) > 0:
                        mods.append(mods_to_send.pop())
                        send_keyboard_event(self.hid_file(), mods_to_send, keys_to_send)
            
                if delay > 0:
                    if logger.getEffectiveLevel() == logging.DEBUG:
                        logger.debug(f"Wait {delay}s before next char type")
                    sleep(delay)

    def press(self, mods: List[int], keys: List[int], release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"mods:{mods},keys:{keys},release={release}")
        send_keyboard_event(self.hid_file(), mods, keys)
        if release:
            self.release()

    def release(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Releasing...")
        send_keyboard_event_identity(self.hid_file())

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()
