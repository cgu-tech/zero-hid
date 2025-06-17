from zero_hid import Mouse
from zero_hid.hid.mouse import relative_mouse_event, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from common import read_bytes, temp_path


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

def test_mouse_move_x_minus16_y1():
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

def test_mouse_move_x_minus18_y1():
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

def test_mouse_move_x0_y1():
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
    assert data == b"\x02\x00\x00\x00\x10\x00\x00\x00"

def test_mouse_movement_only():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 10    # Move right 10 units
            y = -5    # Move up 5 units (negative y)
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    # First byte 0x02 (report ID), second byte 0x00 (no buttons), then x=10 (0x0a), y=-5 (0xfb in two's complement)
    assert data == b"\x02\x00\x0a\xfb\x00\x00\x00\x00"

def test_vertical_wheel_only():
    with temp_path() as dev_path:
        with open(dev_path, "w+b") as dev:
            buttons = []
            x = 0
            y = 0
            vertical_wheel_delta = 1    # Scroll up 1 unit
            horizontal_wheel_delta = 0
            relative_mouse_event(dev, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            dev.seek(0)
            data = dev.read()
    # Vertical wheel delta encoded at 5th byte
    assert data == b"\x02\x00\x00\x00\x01\x00\x00\x00"

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
    assert data == b"\x02\x00\x00\x00\x00\xff\x00\x00"

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

def test_empty_report():
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
