from zero_hid import Keyboard
from zero_hid.hid.keyboard import send_keyboard_event
from zero_hid.hid.keycodes import KeyCodes
from common import read_bytes, temp_path

# To install tests dependencies:
# source ~/venv/bin/activate && pip install pytest

# To run:
# source ~/venv/bin/activate && cd zero-hid
# sudo chmod 755 run_tests.sh && ./run_tests.sh tests/keyboard_test.py

def send_keyboard_event_data(mods, keys):
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            send_keyboard_event(dev, mods, keys)
            dev.seek(0)
            data = dev.read()
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
