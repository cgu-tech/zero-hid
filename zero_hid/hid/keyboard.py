from io import BufferedReader
from . import write as hid_write
import select

KEYBOARD_REPORT_ID = 0x01  # Report ID for Keyboard

def send_keystroke(keyboard_path, control_keys, hid_keycode, release=True):
    buf = [0] * 8
    buf[0] = KEYBOARD_REPORT_ID
    buf[1] = control_keys
    buf[2] = hid_keycode
    hid_write.write_to_hid_interface(keyboard_path, buf)

    # If it's a normal keycode (i.e. not a standalone modifier key), add a
    # message indicating that the key should be released after it is sent.
    if release:
        release_keys(keyboard_path)


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


def release_keys(keyboard_path):
    hid_write.write_to_hid_interface(keyboard_path, [0] * 8)
