# zero_hid/hid/consumer.py

from . import write as hid_write

def send_keystroke(consumer_path, hid_keycode, release=True) -> None:
    buf = [0] * 2
    buf[0] = hid_keycode & 0xFF        # LSB
    buf[1] = (hid_keycode >> 8) & 0xFF # MSB
    hid_write.write_to_hid_interface(consumer_path, buf)

    # If it's a normal keycode (i.e. not a standalone modifier key), add a
    # message indicating that the key should be released after it is sent.
    if release:
        release_keys(consumer_path)

def release_keys(consumer_path):
    buf = [0] * 2
    hid_write.write_to_hid_interface(consumer_path, buf)
