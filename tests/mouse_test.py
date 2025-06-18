from zero_hid import Mouse
from zero_hid.hid.mouse import relative_mouse_event, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from common import read_bytes, temp_path

def get_relative_mouse_event_data(buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta):
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    return data

def test_identity_report():
    data = get_relative_mouse_event_data([], 0, 0, 0, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\x00\x00"

# Tests mouse buttons

def test_mouse_button_left():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_LEFT], 0, 0, 0, 0)
    assert b"\x02\x01\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_RIGHT], 0, 0, 0, 0)
    assert b"\x02\x02\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_middle():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_MIDDLE], 0, 0, 0, 0)
    assert b"\x02\x04\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_left_and_right():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT], 0, 0, 0, 0)
    assert b"\x02\x03\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right_and_left():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_LEFT], 0, 0, 0, 0)
    assert b"\x02\x03\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_left_and_middle():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE], 0, 0, 0, 0)
    assert b"\x02\x05\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_midle_and_left():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_LEFT], 0, 0, 0, 0)
    assert b"\x02\x05\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right_and_midle():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE], 0, 0, 0, 0)
    assert b"\x02\x06\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_midle_and_right():
    data = get_relative_mouse_event_data([MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_RIGHT], 0, 0, 0, 0)
    assert b"\x02\x06\x00\x00\x00\x00\x00\x00" == data

# Tests move X

def test_mouse_move_x_1_y_0():
    data = get_relative_mouse_event_data([], 1, 0, 0, 0)
    assert data == b"\x02\x00\x00\x01\x00\x00\x00\x00"

def test_mouse_move_x_2_y_0():
    data = get_relative_mouse_event_data([], 2, 0, 0, 0)
    assert data == b"\x02\x00\x00\x02\x00\x00\x00\x00"

def test_mouse_move_x_3_y_0():
    data = get_relative_mouse_event_data([], 3, 0, 0, 0)
    assert data == b"\x02\x00\x00\x03\x00\x00\x00\x00"

def test_mouse_move_x_4_y_0():
    data = get_relative_mouse_event_data([], 4, 0, 0, 0)
    assert data == b"\x02\x00\x00\x04\x00\x00\x00\x00"

def test_mouse_move_x_5_y_0():
    data = get_relative_mouse_event_data([], 5, 0, 0, 0)
    assert data == b"\x02\x00\x00\x05\x00\x00\x00\x00"

def test_mouse_move_x_6_y_0():
    data = get_relative_mouse_event_data([], 6, 0, 0, 0)
    assert data == b"\x02\x00\x00\x06\x00\x00\x00\x00"

def test_mouse_move_x_7_y_0():
    data = get_relative_mouse_event_data([], 7, 0, 0, 0)
    assert data == b"\x02\x00\x00\x07\x00\x00\x00\x00"

def test_mouse_move_x_8_y_0():
    data = get_relative_mouse_event_data([], 8, 0, 0, 0)
    assert data == b"\x02\x00\x00\x08\x00\x00\x00\x00"

# Tests move Y

def test_mouse_move_x_0_y_1():
    data = get_relative_mouse_event_data([], 0, 1, 0, 0)
    assert data == b"\x02\x00\x00\x00\x10\x00\x00\x00"

def test_mouse_move_x_0_y_33():
    data = get_relative_mouse_event_data([], 0, 33, 0, 0)
    assert data == b"\x02\x00\x00\x00\x10\x02\x00\x00"

def test_mouse_move_x_0_y_62():
    data = get_relative_mouse_event_data([], 0, 62, 0, 0)
    assert data == b"\x02\x00\x00\x00\xe0\x03\x00\x00"

# Tests move X and Y

def test_mouse_move_x_minus18_y_1():
    data = get_relative_mouse_event_data([], -18, 1, 0, 0)
    assert data == b"\x02\x00\x00\xee\x1f\x00\x00\x00"

def test_mouse_move_x_minus16_y_1():
    data = get_relative_mouse_event_data([], -16, 1, 0, 0)
    assert data == b"\x02\x00\x00\xf0\x1f\x00\x00\x00"

def test_mouse_move_x_minus5_y_62():
    data = get_relative_mouse_event_data([], -5, 62, 0, 0)
    assert data == b"\x02\x00\x00\xfb\xef\x03\x00\x00"

def test_mouse_move_x_minus3_y_68():
    data = get_relative_mouse_event_data([], -3, 68, 0, 0)
    assert data == b"\x02\x00\x00\xfd\x4f\x04\x00\x00"

def test_mouse_move_x_minus2_y_57():
    data = get_relative_mouse_event_data([], -2, 57, 0, 0)
    assert data == b"\x02\x00\x00\xfe\x9f\x03\x00\x00"

def test_mouse_move_x_minus1_y_67():
    data = get_relative_mouse_event_data([], -1, 67, 0, 0)
    assert data == b"\x02\x00\x00\xff\x3f\x04\x00\x00"

def test_mouse_move_x_1_y_1():
    data = get_relative_mouse_event_data([], 1, 1, 0, 0)
    assert data == b"\x02\x00\x00\x01\x10\x00\x00\x00"

def test_mouse_move_x_1_y_29():
    data = get_relative_mouse_event_data([], 1, 29, 0, 0)
    assert data == b"\x02\x00\x00\x01\xd0\x01\x00\x00"

def test_mouse_move_x_2_y_1():
    data = get_relative_mouse_event_data([], 2, 1, 0, 0)
    assert data == b"\x02\x00\x00\x02\x10\x00\x00\x00"

def test_mouse_move_x_2_y_45():
    data = get_relative_mouse_event_data([], 2, 45, 0, 0)
    assert data == b"\x02\x00\x00\x02\xd0\x02\x00\x00"

def test_mouse_move_x_3_y_18():
    data = get_relative_mouse_event_data([], 3, 18, 0, 0)
    assert data == b"\x02\x00\x00\x03\x20\x01\x00\x00"

def test_mouse_move_x_5_y_minus23():
    data = get_relative_mouse_event_data([], 5, -23, 0, 0)
    assert data == b"\x02\x00\x00\x05\x90\xfe\x00\x00"

def test_mouse_move_x_8_y_1():
    data = get_relative_mouse_event_data([], 8, 1, 0, 0)
    assert data == b"\x02\x00\x00\x08\x10\x00\x00\x00"

def test_mouse_move_x_68_y_minus3():
    data = get_relative_mouse_event_data([], 68, -3, 0, 0)
    assert data == b"\x02\x00\x00\x44\xd0\xff\x00\x00"

def test_mouse_move_x_85_y_minus2():
    data = get_relative_mouse_event_data([], 85, -2, 0, 0)
    assert data == b"\x02\x00\x00\x55\xe0\xff\x00\x00"

def test_mouse_move_x_91_y_minus12():
    data = get_relative_mouse_event_data([], 91, -12, 0, 0)
    assert data == b"\x02\x00\x00\x5b\x40\xff\x00\x00"

def test_mouse_move_x_104_y_minus8():
    data = get_relative_mouse_event_data([], 104, -8, 0, 0)
    assert data == b"\x02\x00\x00\x68\x80\xff\x00\x00"

def test_mouse_move_x_118_y_minus13():
    data = get_relative_mouse_event_data([], 118, -13, 0, 0)
    assert data == b"\x02\x00\x00\x76\x30\xff\x00\x00"

def test_mouse_move_x_119_y_minus7():
    data = get_relative_mouse_event_data([], 119, -7, 0, 0)
    assert data == b"\x02\x00\x00\x77\x90\xff\x00\x00"

def test_mouse_move_x_121_y_minus6():
    data = get_relative_mouse_event_data([], 121, -6, 0, 0)
    assert data == b"\x02\x00\x00\x79\xa0\xff\x00\x00"

def test_mouse_move_x_127_y_minus13():
    data = get_relative_mouse_event_data([], 127, -13, 0, 0)
    assert data == b"\x02\x00\x00\x7f\x30\xff\x00\x00"

def test_mouse_move_x_127_y_minus14():
    data = get_relative_mouse_event_data([], 127, -14, 0, 0)
    assert data == b"\x02\x00\x00\x7f\x20\xff\x00\x00"

def test_mouse_move_x_127_y_minus19():
    data = get_relative_mouse_event_data([], 127, -19, 0, 0)
    assert data == b"\x02\x00\x00\x7f\xd0\xfe\x00\x00"

def test_mouse_move_x_127_y_minus21():
    data = get_relative_mouse_event_data([], 127, -21, 0, 0)
    assert data == b"\x02\x00\x00\x7f\xb0\xfe\x00\x00"

# Tests vertical wheel

def test_vertical_wheel_1():
    data = get_relative_mouse_event_data([], 0, 0, 1, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\x01\x00"

def test_vertical_wheel_2():
    data = get_relative_mouse_event_data([], 0, 0, 2, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\x02\x00"

def test_vertical_wheel_3():
    data = get_relative_mouse_event_data([], 0, 0, 3, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\x03\x00"

def test_vertical_wheel_minus1():
    data = get_relative_mouse_event_data([], 0, 0, -1, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\xff\x00"

def test_vertical_wheel_minus2():
    data = get_relative_mouse_event_data([], 0, 0, -2, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\xfe\x00"

def test_vertical_wheel_minus4():
    data = get_relative_mouse_event_data([], 0, 0, -4, 0)
    assert data == b"\x02\x00\x00\x00\x00\x00\xfc\x00"

#def test_horizontal_wheel_only():
#    with temp_path() as dev_path:
#        with open(dev_path, "w+b") as dev:
#            buttons = []
#            x = 0
#            y = 0
#            vertical_wheel_delta = 0
#            horizontal_wheel_delta = -1  # Scroll left 1 unit (two's complement)
#            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
#            dev.seek(0)
#            data = dev.read()
#    # Horizontal wheel delta encoded at 6th byte
#    assert data == b"\x02\x00\x00\x00\x00\x00\x00\x00"
#
#def test_buttons_movement_and_wheel():
#    with temp_path() as dev_path:
#        with open(dev_path, "w+b") as dev:
#            buttons = [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE]
#            x = -20
#            y = 15
#            vertical_wheel_delta = -2
#            horizontal_wheel_delta = 3
#            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
#            dev.seek(0)
#            data = dev.read()
#    # Button mask: 0x01 (left) + 0x04 (middle) = 0x05
#    # x = -20 -> 0xec (two's complement)
#    # y = 15 -> 0x0f
#    # vertical_wheel_delta = -2 -> 0xfe
#    # horizontal_wheel_delta = 3 -> 0x03
#    assert data == b"\x02\x05\xec\x0f\xfe\x03\x00\x00"

