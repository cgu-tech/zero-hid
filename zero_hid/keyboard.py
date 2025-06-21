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
        self.key_map = KeyCodes.as_dict()
        self.set_hid(hid)
        self.common_layout = self.load_layout("common")
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

    def load_layout(self, language):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"language:{language}")
        return json.loads(
            pkgutil.get_data(__name__, f"keymaps/{language}.json").decode()
        )

    def set_layout(self, language):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"language:{language}")
        self.language = language
        self.layout = self.load_layout(language)
        self.build_combos()

    def build_combos(self):
        self.combos = {}

        # Build layout independant combos
        mappings = self.common_layout["Mapping"]
        for combo_name, mapping in mappings.items():
            self.combos[combo_name] = self.build_combo(self.common_layout, combo_name)

        # Build layout specific combos
        # Layout specific combos are allowed to override standard combos
        mappings = self.layout["Mapping"]
        for combo_name, mapping in mappings.items():
            self.combos[combo_name] = self.build_combo(self.layout, combo_name)

    def type(self, text, delay=0):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"text:{text},delay:{delay}")
        if text:
            for c in text:
                if logger.getEffectiveLevel() == logging.DEBUG:
                    logger.debug(f"c:{c}")
                combo = self.combos.get(c)
                if combo is None:
                    raise ValueError(f"No mapping found for character: {c}")
                execute_combo(c, combo)
                if delay > 0:
                    if logger.getEffectiveLevel() == logging.DEBUG:
                        logger.debug(f"Wait {delay}s before next char type")
                    sleep(delay)

    def string_to_code(self, codes_strings):
        # Separate known strings and unknown strings
        codes = []
        unknown_codes = []
        for code_string in codes_strings:
            code = self.key_map.get(code_string)
            if code is not None:
                codes.append(code)
            else:
                unknown_codes.append(mod)

        mapping = {"Codes": codes, "UnknownCodes": unknown_codes}
        return mapping

    def build_combo(self, layout, combo_name):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"combo_name:{combo_name}")
        layout_combo = layout["Mapping"][combo_name]
        if layout_combo is None:
            raise ValueError(f"No mapping found for combo_name: {combo_name}")
    
        # Use layout combos for detected symbol
        combo = []
        is_valid_layout = True
        layout_sequence_index = 0
        for layout_sequence in layout_combo:

            # Retrieve layout_sequence mods and keys names
            layout_mods = layout_sequence["Modifiers"]
            layout_keys = layout_sequence["Keys"]
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(f"combo_name:{combo_name} layout_sequence[{layout_sequence_index}]->mods:{layout_mods},keys:{layout_keys}")

            # Retrieve layout_sequence modifiers and keys codes

            # Separate known modifiers and unknown codes
            sequence_mods = self.string_to_code(layout_mods)
            sequence_keys = self.string_to_code(layout_keys)

            mods = sequence_mods["Codes"]
            keys = sequence_keys["Codes"]

            unknown_mods = sequence_mods["UnknownCodes"]
            unknown_keys = sequence_keys["UnknownCodes"]

            if len(unknown_mods) > 0:
                is_valid_layout = False
                logger.error(f"combo_name:{combo_name} layout_sequence[{layout_sequence_index}]: no matching code found for those modifiers strings: '{unknown_mods}'")
            if len(unknown_keys) > 0:
                is_valid_layout = False
                logger.error(f"combo_name:{combo_name} layout_sequence[{layout_sequence_index}]: no matching code found for those keys strings: '{unknown_keys}'")

            combo.append({"Modifiers": mods, "Keys": keys})
            layout_sequence_index += 1

        if not is_valid_layout:
            raise ValueError(f"Invalid mapping for combo_name: {combo_name}. See error logs for details.")

        return combo

    def execute_combo(self, combo_name, combo):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"combo_name:{combo_name}")

        # Use layout combos for detected symbol
        sequence_index = 0
        for sequence in combo:

            # Retrieve sequence mods and keys names
            mods = sequence["Modifiers"]
            keys = sequence["Keys"]
            if logger.getEffectiveLevel() == logging.DEBUG:
                logger.debug(f"combo_name:{combo_name} sequence[{sequence_index}]->mods:{mods},keys:{keys}")

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

            sequence_index += 1

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

    def combo_switch_app(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Sending combo...")
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_ALT], None)
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_ALT], [KeyCodes.KEY_TAB])
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_ALT], None)
        send_keyboard_event(self.hid_file(), None, None)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Combo send")

    def combo_show_desktop(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Sending combo...")
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], [KeyCodes.KEY_D])
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), None, None)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Combo send")

    def combo_maximize_window(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Sending combo...")
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], [KeyCodes.KEY_UP])
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), None, None)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Combo send")

    def combo_switch_display(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Sending combo...")
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], [KeyCodes.KEY_P])
        send_keyboard_event(self.hid_file(), [KeyCodes.MOD_LEFT_GUI], None)
        send_keyboard_event(self.hid_file(), None, None)
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"Combo send")

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()
