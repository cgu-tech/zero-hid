from zero_hid import Mouse
from zero_hid.hid.mouse import relative_mouse_event, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from common import read_bytes, temp_path

def test_identity_report():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\x00\x00"

# Tests mouse buttons

def test_mouse_button_left():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_LEFT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x01\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_RIGHT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x02\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_middle():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_MIDDLE]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x04\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_left_and_right():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x03\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right_and_left():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_LEFT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x03\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_left_and_middle():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x05\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_midle_and_left():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_LEFT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x05\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_right_and_midle():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x06\x00\x00\x00\x00\x00\x00" == data

def test_mouse_button_midle_and_right():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_MIDDLE, MOUSE_BUTTON_RIGHT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert b"\x02\x06\x00\x00\x00\x00\x00\x00" == data

# Tests move X

def test_mouse_move_x_1_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 1
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x01\x00\x00\x00\x00"

def test_mouse_move_x_2_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 2
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x02\x00\x00\x00\x00"

def test_mouse_move_x_3_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 3
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x03\x00\x00\x00\x00"

def test_mouse_move_x_4_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 4
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x04\x00\x00\x00\x00"

def test_mouse_move_x_5_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 5
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x05\x00\x00\x00\x00"

def test_mouse_move_x_6_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 6
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x06\x00\x00\x00\x00"

def test_mouse_move_x_7_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 7
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x07\x00\x00\x00\x00"

def test_mouse_move_x_8_y_0():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 8
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x08\x00\x00\x00\x00"

# Tests move Y

def test_mouse_move_x_0_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x10\x00\x00\x00"

# Tests move X and Y

def test_mouse_move_x_1_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 1
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x01\x10\x00\x00\x00"

def test_mouse_move_x_2_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 2
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x02\x10\x00\x00\x00"

def test_mouse_move_x_8_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 8
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x08\x10\x00\x00\x00"

def test_mouse_move_x_minus16_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = -16
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\xf0\x1f\x00\x00\x00"

def test_mouse_move_x_minus18_y_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = -18
            y = 1
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\xee\x1f\x00\x00\x00"

# Tests vertical wheel

def test_vertical_wheel_1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 1
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\x01\x00"

def test_vertical_wheel_2():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 2
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\x02\x00"

def test_vertical_wheel_3():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 3
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\x03\x00"

def test_vertical_wheel_minus1():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = -1
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\xff\x00"

def test_vertical_wheel_minus2():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = -2
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\xfe\x00"

def test_vertical_wheel_minus4():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = -4
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    assert data == b"\x02\x00\x00\x00\x00\x00\xfc\x00"

def test_horizontal_wheel_only():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = -1  # Scroll left 1 unit (two's complement)
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    # Horizontal wheel delta encoded at 6th byte
    assert data == b"\x02\x00\x00\x00\x00\x00\x00\x00"

def test_buttons_movement_and_wheel():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = [MOUSE_BUTTON_LEFT, MOUSE_BUTTON_MIDDLE]
            x = -20
            y = 15
            vertical_wheel_delta = -2
            horizontal_wheel_delta = 3
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    # Button mask: 0x01 (left) + 0x04 (middle) = 0x05
    # x = -20 -> 0xec (two's complement)
    # y = 15 -> 0x0f
    # vertical_wheel_delta = -2 -> 0xfe
    # horizontal_wheel_delta = 3 -> 0x03
    assert data == b"\x02\x05\xec\x0f\xfe\x03\x00\x00"

