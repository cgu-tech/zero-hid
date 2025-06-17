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
