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

# Bit 0: Num Lock
# Bit 1: Caps Lock
# Bit 2: Scroll Lock
# Bit 3: Compose
# Bit 4: Kana
# Bits 5-7: Padding (unused)
def read_keyboard_state(dev, timeout=0.1):
    """
    Non-blocking read of the LED state from Report ID 14 on the HID gadget.

    :param dev: file-like object opened in "r+b" mode on HID device
    :param timeout: seconds to wait for data before returning None
    :return: int with LED bits (0-31), or None if no data available
    """
    # Check if device is ready for reading
    rlist, _, _ = select.select([dev], [], [], timeout)
    if not rlist:
        # No data available within timeout
        return None

    # Data is available, attempt to read
    try:
        dev.seek(0)
        data = dev.read(2)
        if len(data) != 2 or data[0] != 0x0E:
            return None  # Invalid report

        state = data[1] & 0b00011111
        return state

    except Exception:
        return None
