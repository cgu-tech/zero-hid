from zero_hid import Device, Keyboard
from zero_hid.hid.keyboard import send_keyboard_event
from zero_hid.hid.keycodes import KeyCodes
from common import read_bytes, temp_path

# To install tests dependencies:
# source ~/venv/bin/activate && pip install pytest

# To run:
# source ~/venv/bin/activate && cd zero-hid
# sudo chmod 755 run_tests.sh && ./run_tests.sh tests/keyboard_test.py

def create_empty_file(dev_path):
    with open(dev_path, "w") as f:
        f.write("")

def send_keyboard_event_data(mods, keys):
    with temp_path() as dev_path:
        create_empty_file(dev_path)
        with Device(dev_path) as dev:
            hid_file = dev.get_file()
            send_keyboard_event(hid_file, mods, keys)
            hid_file.seek(0)
            data = hid_file.read()
    return data

# Test keyboard identity

def test_identity_report():
    data = send_keyboard_event_data(None, None)
    assert data == b"\x01\x00\x00\x00\x00\x00\x00\x00"

# Tests keyboard modifiers unique

def test_keyboard_modifier_leftcontrol():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL], None)
    assert data == b"\x01\x01\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftshift():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_ALT], None)
    assert data == b"\x01\x04\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x08\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_rightcontrol():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_CONTROL], None)
    assert data == b"\x01\x10\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_rightshift():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_SHIFT], None)
    assert data == b"\x01\x20\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x40\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_rightgui():
    data = send_keyboard_event_data([KeyCodes.MOD_RIGHT_GUI], None)
    assert data == b"\x01\x80\x00\x00\x00\x00\x00\x00"

# Tests keyboard modifiers multiple

def test_keyboard_modifier_leftcontrol_leftshift():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x03\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftshift_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0b\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0f\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4f\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftshift_leftalt_leftgui_rightcontrol_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_CONTROL, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5f\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftalt_leftgui_rightcontrol_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_CONTROL, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5d\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftcontrol_leftalt_leftgui_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_LEFT_GUI, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4d\x00\x00\x00\x00\x00\x00"

def test_keyboard_modifier_leftalt_rightalt():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_ALT, KeyCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x44\x00\x00\x00\x00\x00\x00"

# Tests keyboard keys single

def test_keyboard_key_q():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_keyboard_key_w():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_W])
    assert data == b"\x01\x00\x1a\x00\x00\x00\x00\x00"

def test_keyboard_key_e():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_E])
    assert data == b"\x01\x00\x08\x00\x00\x00\x00\x00"

def test_keyboard_key_r():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_R])
    assert data == b"\x01\x00\x15\x00\x00\x00\x00\x00"

def test_keyboard_key_t():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_T])
    assert data == b"\x01\x00\x17\x00\x00\x00\x00\x00"

def test_keyboard_key_y():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Y])
    assert data == b"\x01\x00\x1c\x00\x00\x00\x00\x00"

# Tests keyboard modifiers single and keys single

def test_keyboard_leftshift_key_q():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Q])
    assert data == b"\x01\x02\x14\x00\x00\x00\x00\x00"

def test_keyboard_leftshift_key_w():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_W])
    assert data == b"\x01\x02\x1a\x00\x00\x00\x00\x00"

def test_keyboard_leftshift_key_e():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_E])
    assert data == b"\x01\x02\x08\x00\x00\x00\x00\x00"

def test_keyboard_leftshift_key_r():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_R])
    assert data == b"\x01\x02\x15\x00\x00\x00\x00\x00"

def test_keyboard_leftshift_key_t():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_T])
    assert data == b"\x01\x02\x17\x00\x00\x00\x00\x00"

def test_keyboard_leftshift_key_y():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Y])
    assert data == b"\x01\x02\x1c\x00\x00\x00\x00\x00"

# Tests keyboard modifiers multiple and keys single

def test_keyboard_leftcontrol_leftshift_key_q():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Q])
    assert data == b"\x01\x03\x14\x00\x00\x00\x00\x00"

def test_keyboard_leftcontrol_leftshift_key_w():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_W])
    assert data == b"\x01\x03\x1a\x00\x00\x00\x00\x00"

def test_keyboard_leftcontrol_leftshift_key_e():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_E])
    assert data == b"\x01\x03\x08\x00\x00\x00\x00\x00"

def test_keyboard_leftcontrol_leftshift_key_r():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_R])
    assert data == b"\x01\x03\x15\x00\x00\x00\x00\x00"

def test_keyboard_leftcontrol_leftshift_key_t():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_T])
    assert data == b"\x01\x03\x17\x00\x00\x00\x00\x00"

def test_keyboard_leftcontrol_leftshift_key_y():
    data = send_keyboard_event_data([KeyCodes.MOD_LEFT_CONTROL, KeyCodes.MOD_LEFT_SHIFT], [KeyCodes.KEY_Y])
    assert data == b"\x01\x03\x1c\x00\x00\x00\x00\x00"

# Tests keyboard keys multiple

def test_keyboard_key_q():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_keyboard_key_q_key_w():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W])
    assert data == b"\x01\x00\x14\x1a\x00\x00\x00\x00"

def test_keyboard_key_q_key_w_key_e():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E])
    assert data == b"\x01\x00\x14\x1a\x08\x00\x00\x00"

def test_keyboard_key_q_key_w_key_e_key_r():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x00\x00"

def test_keyboard_key_q_key_w_key_e_key_r_key_t():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R, KeyCodes.KEY_T])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x17\x00"

def test_keyboard_key_q_key_w_key_e_key_r_key_t_key_y():
    data = send_keyboard_event_data(None, [KeyCodes.KEY_Q, KeyCodes.KEY_W, KeyCodes.KEY_E, KeyCodes.KEY_R, KeyCodes.KEY_T, KeyCodes.KEY_Y])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x17\x1c"



#def test_typing():
#    with temp_path() as p:
#        k = Keyboard(p)
#        k.type("Hello world!")
#        data = read_bytes(p)
#    expect = b"\x02\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x1e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
#    assert expect == data
#
#
#def test_release():
#    with temp_path() as p:
#        k = Keyboard(p)
#        k.release()
#        data = read_bytes(p)
#
#    assert b"\x00\x00\x00\x00\x00\x00\x00\x00" == data
