from . import write as hid_write
from functools import reduce
import operator
from typing import List, TypedDict
import os
import select

KEYBOARD_STATE_NONE = 0b00000
KEYBOARD_REPORT_ID = 0x01  # Report ID for Keyboard

class LEDState(TypedDict):
    num_lock: bool
    caps_lock: bool
    scroll_lock: bool
    compose: bool
    kana: bool

def pack_keys(keys: List[int]) -> List[int]:
    """Pack a signed integer value into 12 bits 2's complement."""
    if not keys:
        return []
    if len(keys) > 6:
        raise ValueError("Too many keyboard keys: HID supports up to 6 simultaneous key presses.")
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

    # 6 keys: 48 bits (6 bytes)
    keys = pack_keys(keys)
    i = 2
    for key in keys:
        buf[i] = key
        i += 1

    # Send keyboard event
    hid_write.write_to_hid_interface(dev, buf)

def send_keyboard_event_identity(dev):
    send_keyboard_event(dev, None, None)

def read_keyboard_state(dev, timeout=0.1) -> int | None:
    """
    Reads the LED output report (Report ID 0x0E) from the HID device in non-blocking mode.

    Parameters:
        dev (file-like object): An open HID device in 'r+b' mode.

    Returns:
        int | None: A byte representing the LED bitfield if available, or None if no data.
    """
    # Set the file descriptor to non-blocking
    fd = dev.fileno()
    fl = os.O_NONBLOCK
    orig_fl = os.get_blocking(fd)
    os.set_blocking(fd, False)

    try:
        # Wait up to 100ms for data to be ready
        rlist, _, _ = select.select([dev], [], [], timeout)
        if not rlist:
            return None

        # Attempt to read 2 bytes (Report ID + LED bits)
        data = dev.read(2)
        if data and len(data) == 2 and data[0] == 0x0E:
            # Bit 0: Num Lock
            # Bit 1: Caps Lock
            # Bit 2: Scroll Lock
            # Bit 3: Compose
            # Bit 4: Kana
            # Bits 5-7: Padding (unused)
            return data[1] & 0b00011111
    except BlockingIOError:
        pass
    finally:
        os.set_blocking(fd, orig_fl)

    return None

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
