from . import write as hid_write
from typing import List

CONSUMER_REPORT_ID = 0x03  # Report ID for Consumer Control

def pack_keys(keys: List[int]) -> List[int]:
    """Pack a signed integer value into 12 bits 2's complement."""
    if not keys:
        return []
    if len(keys) > 2:
        raise ValueError("Too many consumer keys: HID supports up to 2 simultaneous key presses.")
    return keys

def send_consumer_event(hid_file, keys: List[int]) -> None:
    # Create Consumer report buffer
    buf = [0] * 5

    # Report ID 3: 8 bits (1 byte)
    buf[0] = CONSUMER_REPORT_ID

    # 2 keys (16 bits per key, little endian): 32 bits (4 bytes)
    keys = pack_keys(keys)
    i = 1
    for key in keys:
        buf[i] = key & 0xFF         # low byte
        i += 1
        buf[i] = (key >> 8) & 0xFF  # high byte
        i += 1

    hid_write.write_to_hid_interface(hid_file, buf)

def send_consumer_event_identity(hid_file):
    send_consumer_event(hid_file, None)
