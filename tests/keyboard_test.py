from zero_hid import Device, Keyboard
from zero_hid.hid.keyboard import send_keyboard_event
from zero_hid.hid.keycodes import KeyCodes
from common import read_bytes, temp_path
from mockdevice import MockDevice
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# To install tests dependencies:
# source ~/venv/bin/activate && pip install pytest

# To run:
# source ~/venv/bin/activate && cd zero-hid
# sudo chmod 755 run_tests.sh && ./run_tests.sh tests/keyboard_test.py

# Utilities

def create_empty_file(dev_path):
    with open(dev_path, "w") as f:
        f.write("")

def get_device_data(callback):
    with MockDevice() as dev:
        hid_file = dev.get_file()
        callback(dev)
        hid_file.seek_for_test(0)
        data = hid_file.read()
    return data

def send_keyboard_event_data(mods, keys):
    return get_device_data(lambda dev: send_keyboard_event_data_callback(dev, mods, keys))
def send_keyboard_event_data_callback(dev, mods, keys):
    send_keyboard_event(dev.get_file(), mods, keys)

def type_data(language, text):
    return get_device_data(lambda dev: type_data_callback(dev, language, text))
def type_data_callback(dev, language, text):
    kb = Keyboard(dev, language)
    kb.type(text)

def press_data(mods, keys, release):
    return get_device_data(lambda dev: press_data_callback(dev, mods, keys, release))
def press_data_callback(dev, mods, keys, release):
    kb = Keyboard(dev)
    kb.press(mods, keys, release)

def combo_switch_app_data():
    return get_device_data(lambda dev: combo_switch_app_data_callback(dev))
def combo_switch_app_data_callback(dev):
    kb = Keyboard(dev)
    kb.combo_switch_app()

def combo_show_desktop_data():
    return get_device_data(lambda dev: combo_show_desktop_data_callback(dev))
def combo_show_desktop_data_callback(dev):
    kb = Keyboard(dev)
    kb.combo_show_desktop()

def combo_maximize_window_data():
    return get_device_data(lambda dev: combo_maximize_window_data_callback(dev))
def combo_maximize_window_data_callback(dev):
    kb = Keyboard(dev)
    kb.combo_maximize_window()

def combo_switch_display_data():
    return get_device_data(lambda dev: combo_switch_display_data_callback(dev))
def combo_switch_display_data_callback(dev):
    kb = Keyboard(dev)
    kb.combo_switch_display()

# Test HID keyboard identity

def test_hid_keyboard_identity_report():
    data = send_keyboard_event_data(None, None)
    assert data == b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests HID keyboard modifiers unique

def test_hid_keyboard_modifier_leftcontrol():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL], None)
    assert data == b"\x01\x01\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftshift():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_ALT], None)
    assert data == b"\x01\x04\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x08\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_rightcontrol():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_CONTROL], None)
    assert data == b"\x01\x10\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_rightshift():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_SHIFT], None)
    assert data == b"\x01\x20\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x40\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_rightgui():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_GUI], None)
    assert data == b"\x01\x80\x00\x00\x00\x00\x00\x00"

# Tests HID keyboard modifiers multiple

def test_hid_keyboard_modifier_leftcontrol_leftshift():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x03\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftshift_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0b\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0f\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4f\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui_rightcontrol_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_CONTROL, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5f\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftalt_leftgui_rightcontrol_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_CONTROL, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5d\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftcontrol_leftalt_leftgui_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4d\x00\x00\x00\x00\x00\x00"

def test_hid_keyboard_modifier_leftalt_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x44\x00\x00\x00\x00\x00\x00"

# Tests HID keyboard keys single

def test_hid_keyboard_key_q():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_w():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_W])
    assert data == b"\x01\x00\x1a\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_e():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_E])
    assert data == b"\x01\x00\x08\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_r():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_R])
    assert data == b"\x01\x00\x15\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_t():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_T])
    assert data == b"\x01\x00\x17\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_y():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Y])
    assert data == b"\x01\x00\x1c\x00\x00\x00\x00\x00"

# Tests HID keyboard modifiers single and keys single

def test_hid_keyboard_leftshift_key_q():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Q])
    assert data == b"\x01\x02\x14\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftshift_key_w():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_W])
    assert data == b"\x01\x02\x1a\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftshift_key_e():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_E])
    assert data == b"\x01\x02\x08\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftshift_key_r():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_R])
    assert data == b"\x01\x02\x15\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftshift_key_t():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_T])
    assert data == b"\x01\x02\x17\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftshift_key_y():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Y])
    assert data == b"\x01\x02\x1c\x00\x00\x00\x00\x00"

# Tests HID keyboard modifiers multiple and keys single

def test_hid_keyboard_leftcontrol_leftshift_key_q():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Q])
    assert data == b"\x01\x03\x14\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftcontrol_leftshift_key_w():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_W])
    assert data == b"\x01\x03\x1a\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftcontrol_leftshift_key_e():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_E])
    assert data == b"\x01\x03\x08\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftcontrol_leftshift_key_r():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_R])
    assert data == b"\x01\x03\x15\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftcontrol_leftshift_key_t():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_T])
    assert data == b"\x01\x03\x17\x00\x00\x00\x00\x00"

def test_hid_keyboard_leftcontrol_leftshift_key_y():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Y])
    assert data == b"\x01\x03\x1c\x00\x00\x00\x00\x00"

# Tests HID keyboard keys multiple

def test_hid_keyboard_key_q():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_hid_keyboard_key_q_key_w():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W])
    assert data == b"\x01\x00\x14\x1a\x00\x00\x00\x00"

def test_hid_keyboard_key_q_key_w_key_e():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E])
    assert data == b"\x01\x00\x14\x1a\x08\x00\x00\x00"

def test_hid_keyboard_key_q_key_w_key_e_key_r():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x00\x00"

def test_hid_keyboard_key_q_key_w_key_e_key_r_key_t():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R, KeyCodes.KEY_T])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x17\x00"

def test_hid_keyboard_key_q_key_w_key_e_key_r_key_t_key_y():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R, KeyCodes.KEY_T, KeyCodes.KEY_Y])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x17\x1c"

# Tests keyboard type keys unique, US layout

def test_keyboard_type_us_none():
    data = type_data("US", None)
    assert data == b""

def test_keyboard_type_us_empty():
    data = type_data("US", "")
    assert data == b""

def test_keyboard_type_us_q():
    data = type_data("US", "q")
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_w():
    data = type_data("US", "w")
    assert data == b"\x01\x00\x1a\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_e():
    data = type_data("US", "e")
    assert data == b"\x01\x00\x08\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_r():
    data = type_data("US", "r")
    assert data == b"\x01\x00\x15\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_t():
    data = type_data("US", "t")
    assert data == b"\x01\x00\x17\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_y():
    data = type_data("US", "y")
    assert data == b"\x01\x00\x1c\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests keyboard type keys multiple, US layout

def test_keyboard_type_us_Q():
    data = type_data("US", "Q")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x14\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_W():
    data = type_data("US", "W")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x1a\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_E():
    data = type_data("US", "E")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x08\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_R():
    data = type_data("US", "R")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x15\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_T():
    data = type_data("US", "T")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x17\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_us_Y():
    data = type_data("US", "Y")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x1c\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests keyboard type keys unique, FR layout

def test_keyboard_type_fr_none():
    data = type_data("FR", None)
    assert data == b""

def test_keyboard_type_fr_empty():
    data = type_data("FR", "")
    assert data == b""

def test_keyboard_type_fr_a():
    data = type_data("FR", "a")
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_z():
    data = type_data("FR", "z")
    assert data == b"\x01\x00\x1a\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_e():
    data = type_data("FR", "e")
    assert data == b"\x01\x00\x08\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_r():
    data = type_data("FR", "r")
    assert data == b"\x01\x00\x15\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_t():
    data = type_data("FR", "t")
    assert data == b"\x01\x00\x17\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_y():
    data = type_data("FR", "y")
    assert data == b"\x01\x00\x1c\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests keyboard type keys multiple, FR layout

def test_keyboard_type_fr_A():
    data = type_data("FR", "A")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x14\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_Z():
    data = type_data("FR", "Z")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x1a\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_E():
    data = type_data("FR", "E")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x08\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_R():
    data = type_data("FR", "R")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x15\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_T():
    data = type_data("FR", "T")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x17\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

def test_keyboard_type_fr_Y():
    data = type_data("FR", "Y")
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x02\x1c\x00\x00\x00\x00\x00" + b"\x01\x02\x00\x00\x00\x00\x00\x00" + b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests keyboard combos, FR layout

def test_keyboard_type_fr_A_umlaut():
    data = type_data("FR", "Ä")
    assert data == (
        b"\x01\x02\x00\x00\x00\x00\x00\x00" +
        b"\x01\x02\x2f\x00\x00\x00\x00\x00" +
        b"\x01\x02\x00\x00\x00\x00\x00\x00" +
        b"\x01\x00\x00\x00\x00\x00\x00\x00" +
        b"\x01\x02\x00\x00\x00\x00\x00\x00" + 
        b"\x01\x02\x14\x00\x00\x00\x00\x00" + 
        b"\x01\x02\x00\x00\x00\x00\x00\x00" + 
        b"\x01\x00\x00\x00\x00\x00\x00\x00"
    )


# Test keyboard press unique


def test_keyboard_press_application():
    data = press_data(None,[KeyCodes.KEY_COMPOSE])
    assert data == b"\x01\x00\x65\x00\x00\x00\x00\x00"
    data = press_data(None,None)
    assert data == b"\x01\x00\x00\x00\x00\x00\x00\x00"



# Tests keyboard hardcoded combos


# switch app: LeftAlt (0x04) + Tab (0x2b)
def test_keyboard_combo_switch_app():
    data = combo_switch_app_data()
    assert data == (
        b"\x01\x04\x00\x00\x00\x00\x00\x00" +
        b"\x01\x04\x2b\x00\x00\x00\x00\x00" +
        b"\x01\x04\x00\x00\x00\x00\x00\x00" +
        b"\x01\x00\x00\x00\x00\x00\x00\x00"
    )

# reduce all and show desktop: Left GUI (0x08) + 'd and D' (0x07)
def test_keyboard_type_fr_show_desktop():
    data = combo_show_desktop_data()
    assert data == (
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x08\x07\x00\x00\x00\x00\x00" +
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x00\x00\x00\x00\x00\x00\x00"
    )

# maximize: Left GUI (0x08) + UpArrow (0x52)
def test_keyboard_combo_maximize_window():
    data = combo_maximize_window_data()
    assert data == (
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x08\x52\x00\x00\x00\x00\x00" +
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x00\x00\x00\x00\x00\x00\x00"
    )

# switch display: Left GUI (0x08) + 'p and P' (0x13)
def test_keyboard_combo_switch_display():
    data = combo_switch_display_data()
    assert data == (
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x08\x13\x00\x00\x00\x00\x00" +
        b"\x01\x08\x00\x00\x00\x00\x00\x00" +
        b"\x01\x00\x00\x00\x00\x00\x00\x00"
    )
