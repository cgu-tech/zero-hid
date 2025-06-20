from zero_hid import Consumer
from zero_hid.hid.consumer import send_consumer_event
from zero_hid.hid.consumercodes import ConsumerCodes
from common import read_bytes, temp_path

# To install tests dependencies:
# source ~/venv/bin/activate && pip install pytest

# To run:
# source ~/venv/bin/activate && cd zero-hid
# sudo chmod 755 run_tests.sh && ./run_tests.sh tests/consumer_test.py

def send_consumer_event_data(mods, keys):
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            send_consumer_event(dev, mods, keys)
            dev.seek(0)
            data = dev.read()
    return data

# Test keyboard identity

def test_identity_report():
    data = send_consumer_event_data(None)
    assert data == b"\x03\x00\x00\x00\x00"

# Tests keyboard modifiers unique

def test_consumer_modifier_leftcontrol():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL], None)
    assert data == b"\x01\x01\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftshift():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x02\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_ALT], None)
    assert data == b"\x01\x04\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftgui():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x08\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_rightcontrol():
    data = send_consumer_event_data([ConsumerCodes.MOD_RIGHT_CONTROL], None)
    assert data == b"\x01\x10\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_rightshift():
    data = send_consumer_event_data([ConsumerCodes.MOD_RIGHT_SHIFT], None)
    assert data == b"\x01\x20\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x40\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_rightgui():
    data = send_consumer_event_data([ConsumerCodes.MOD_RIGHT_GUI], None)
    assert data == b"\x01\x80\x00\x00\x00\x00\x00\x00"

# Tests keyboard modifiers multiple

def test_consumer_modifier_leftcontrol_leftshift():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], None)
    assert data == b"\x01\x03\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftshift_leftgui():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT, ConsumerCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0b\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftshift_leftalt_leftgui():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT, ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_LEFT_GUI], None)
    assert data == b"\x01\x0f\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftshift_leftalt_leftgui_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT, ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_LEFT_GUI, ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4f\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftshift_leftalt_leftgui_rightcontrol_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT, ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_LEFT_GUI, ConsumerCodes.MOD_RIGHT_CONTROL, ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5f\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftalt_leftgui_rightcontrol_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_LEFT_GUI, ConsumerCodes.MOD_RIGHT_CONTROL, ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x5d\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftcontrol_leftalt_leftgui_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_LEFT_GUI, ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x4d\x00\x00\x00\x00\x00\x00"

def test_consumer_modifier_leftalt_rightalt():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_ALT, ConsumerCodes.MOD_RIGHT_ALT], None)
    assert data == b"\x01\x44\x00\x00\x00\x00\x00\x00"

# Tests keyboard keys single

def test_consumer_key_q():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_consumer_key_w():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_W])
    assert data == b"\x01\x00\x1a\x00\x00\x00\x00\x00"

def test_consumer_key_e():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_E])
    assert data == b"\x01\x00\x08\x00\x00\x00\x00\x00"

def test_consumer_key_r():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_R])
    assert data == b"\x01\x00\x15\x00\x00\x00\x00\x00"

def test_consumer_key_t():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_T])
    assert data == b"\x01\x00\x17\x00\x00\x00\x00\x00"

def test_consumer_key_y():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Y])
    assert data == b"\x01\x00\x1c\x00\x00\x00\x00\x00"

# Tests keyboard modifiers single and keys single

def test_consumer_leftshift_key_q():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_Q])
    assert data == b"\x01\x02\x14\x00\x00\x00\x00\x00"

def test_consumer_leftshift_key_w():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_W])
    assert data == b"\x01\x02\x1a\x00\x00\x00\x00\x00"

def test_consumer_leftshift_key_e():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_E])
    assert data == b"\x01\x02\x08\x00\x00\x00\x00\x00"

def test_consumer_leftshift_key_r():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_R])
    assert data == b"\x01\x02\x15\x00\x00\x00\x00\x00"

def test_consumer_leftshift_key_t():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_T])
    assert data == b"\x01\x02\x17\x00\x00\x00\x00\x00"

def test_consumer_leftshift_key_y():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_Y])
    assert data == b"\x01\x02\x1c\x00\x00\x00\x00\x00"

# Tests keyboard modifiers multiple and keys single

def test_consumer_leftcontrol_leftshift_key_q():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_Q])
    assert data == b"\x01\x03\x14\x00\x00\x00\x00\x00"

def test_consumer_leftcontrol_leftshift_key_w():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_W])
    assert data == b"\x01\x03\x1a\x00\x00\x00\x00\x00"

def test_consumer_leftcontrol_leftshift_key_e():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_E])
    assert data == b"\x01\x03\x08\x00\x00\x00\x00\x00"

def test_consumer_leftcontrol_leftshift_key_r():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_R])
    assert data == b"\x01\x03\x15\x00\x00\x00\x00\x00"

def test_consumer_leftcontrol_leftshift_key_t():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_T])
    assert data == b"\x01\x03\x17\x00\x00\x00\x00\x00"

def test_consumer_leftcontrol_leftshift_key_y():
    data = send_consumer_event_data([ConsumerCodes.MOD_LEFT_CONTROL, ConsumerCodes.MOD_LEFT_SHIFT], [ConsumerCodes.KEY_Y])
    assert data == b"\x01\x03\x1c\x00\x00\x00\x00\x00"

# Tests keyboard keys multiple

def test_consumer_key_q():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q])
    assert data == b"\x01\x00\x14\x00\x00\x00\x00\x00"

def test_consumer_key_q_key_w():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q, ConsumerCodes.KEY_W])
    assert data == b"\x01\x00\x14\x1a\x00\x00\x00\x00"

def test_consumer_key_q_key_w_key_e():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q, ConsumerCodes.KEY_W, ConsumerCodes.KEY_E])
    assert data == b"\x01\x00\x14\x1a\x08\x00\x00\x00"

def test_consumer_key_q_key_w_key_e_key_r():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q, ConsumerCodes.KEY_W, ConsumerCodes.KEY_E, ConsumerCodes.KEY_R])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x00\x00"

def test_consumer_key_q_key_w_key_e_key_r_key_t():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q, ConsumerCodes.KEY_W, ConsumerCodes.KEY_E, ConsumerCodes.KEY_R, ConsumerCodes.KEY_T])
    assert data == b"\x01\x00\x14\x1a\x08\x15\x17\x00"

def test_consumer_key_q_key_w_key_e_key_r_key_t_key_y():
    data = send_consumer_event_data(None, [ConsumerCodes.KEY_Q, ConsumerCodes.KEY_W, ConsumerCodes.KEY_E, ConsumerCodes.KEY_R, ConsumerCodes.KEY_T, ConsumerCodes.KEY_Y])
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
