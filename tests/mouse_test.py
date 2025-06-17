from zero_hid import Mouse
from zero_hid.hid.mouse import relative_mouse_event, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from common import read_bytes, temp_path


def test_mouse_button_left():
    with temp_path() as p:
        with open(path, "r+b") as f:
            buttons = [MOUSE_BUTTON_LEFT]
            x = 0
            y = 0
            vertical_wheel_delta = 0
            horizontal_wheel_delta = 0
            relative_mouse_event(p, buttons, x, y, vertical_wheel_delta, horizontal_wheel_delta)
            f.seek(0)
            data = f.read()
    assert b"\x02\x00\x01\x00\x00\x00\x00\x00" == data

