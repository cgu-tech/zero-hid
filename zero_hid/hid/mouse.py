from . import write as hid_write
from functools import reduce
import operator
from typing import List

MOUSE_REPORT_ID     = 0x02  # Report ID for Mouse
MOUSE_BUTTON_LEFT   = 0x01  # Mouse button code left
MOUSE_BUTTON_RIGHT  = 0x02  # Mouse button code right
MOUSE_BUTTON_MIDDLE = 0x04  # Mouse button code middle

def pack_signed_12bit(value):
    """Pack a signed integer value into 12 bits 2's complement."""
    if not (-2047 <= value <= 2047):
        raise ValueError("Value out of 12-bit signed range")
    if value < 0:
        value = (1 << 12) + value  # 2's complement
    return value

def reduce_values(values: List[int]):
    if not values:
        return 0x00
    if len(values) == 1:
        values = values[0]
    else:
        values = reduce(operator.or_, values, 0)
    return values

def send_mouse_event(dev, buttons: List[int], x, y, scroll_x, scroll_y):
    # Create Mouse report buffer
    buf = [0] * 8

    # Report ID 2: 8 bits (1 byte)
    buf[0] = MOUSE_REPORT_ID

    # Buttons: 16 bits (2 bytes)
    buttons = reduce_values(buttons)
    buf[1] = buttons & 0xFF          # Low byte buttons
    buf[2] = (buttons >> 8) & 0xFF   # High byte buttons

    # X and Y deltas: 24 bits (3 bytes)

    # Pack signed 12-bit X and Y
    x12 = pack_signed_12bit(x)
    y12 = pack_signed_12bit(y)

    # X: 12 bits (1.5 byte)
    # bits 0-7 in buf[3], bits 8-11 in lower nibble of buf[4]
    buf[3] = x12 & 0xFF
    buf[4] = (x12 >> 8) & 0x0F

    # Y: 12 bits (1.5 byte)
    # bits 0-3 in upper nibble of buf[4], bits 4-11 in buf[5]
    buf[4] |= (y12 & 0x0F) << 4
    buf[5] = (y12 >> 4) & 0xFF

    # Scroll Y (Wheel): 8 bits (1 byte)
    # Signed value to unsigned value
    buf[6] = scroll_y & 0xFF

    # Scroll X (AC Pan): 8-bit (1 byte)
    # Signed value to unsigned value
    buf[7] = scroll_x & 0xFF

    # Write the buffer to HID device
    hid_write.write_to_hid_interface(dev, buf)

def send_mouse_event_identity(dev):
    send_mouse_event(dev, None, 0, 0, 0, 0)
