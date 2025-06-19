from io import BufferedReader
from . import write as hid_write
from functools import reduce
import operator
from typing import List
import select

KEYBOARD_REPORT_ID = 0x01  # Report ID for Keyboard

def pack_keys(keys: List[int]) -> List[int]:
    """Pack a signed integer value into 12 bits 2's complement."""
    if not keys:
        return []
    if len(keys) > 6:
        raise ValueError("Too many keys: HID supports up to 6 simultaneous key presses.")
    return keys

def reduce_values(values: List[int]):
    if not values:
        return 0x00
    if len(values) == 1:
        values = values[0]
    else:
        values = reduce(operator.or_, values, 0)
    return values

def send_keyboard_event(dev, mods: List[int], keys: List[int]):
    # Create Keyboard report buffer
    buf = [0] * 8

    # Report ID 1: 8 bits (1 byte)
    buf[0] = KEYBOARD_REPORT_ID

    # mods (Left/Right Control, Left/Right Shift, Left/Right Alt, Left/Right Gui): 8 bits (1 byte)
    mods = reduce_values(mods)
    buf[1] = mods

    # 6 keys: 48 bits (8 bytes)
    keys = pack_keys(keys)
    i = 2
    for key in keys:
        buf[i] = key
        i += 1

    # Send keyboard event
    hid_write.write_to_hid_interface(dev, buf)

def send_keyboard_event_identity(dev):
    send_keyboard_event(dev, None, None)

def read_last_report(keyboard: "BufferedReader", size: int):
    #if isinstance(keyboard, str):
    #    keyboard = open(keyboard, "rb")
    #has_data = select.select([keyboard], [], [], 0.1)[0] != []
    #if has_data:
    #    while select.select([keyboard], [], [], 0.1)[0] != []:
    #        buf = keyboard.read(size)
    #else:
    #    buf = keyboard.read(size)
    #TODO: rework this part with new HID interface
    buf = [0] * 1
    return buf
