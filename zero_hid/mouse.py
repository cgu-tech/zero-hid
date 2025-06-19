from . import defaults
from .hid.mouse import raise_mouse_event, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from typing import SupportsInt, List


MOUSE_BUTTONS_NONE   = []  # No mouse buttons

class RelativeMoveRangeError(Exception):
    pass


class Mouse:
    def __init__(self, dev=None) -> None:
        self.__setup_device(dev)
        self.buttons_state = MOUSE_BUTTONS_NONE

    def __setup_device(self, dev):
        if dev is None:
            dev = defaults.MOUSE_PATH
        if not hasattr(dev, "write"):  # check if file like object
            self.dev = open(dev, "ab+")
        else:
            self.dev = dev

    def left_click(self, release=True):
        self.buttons_click([MOUSE_BUTTON_LEFT], release)

    def right_click(self, release=True):
        self.buttons_click([MOUSE_BUTTON_RIGHT], release)

    def middle_click(self, release=True):
        self.buttons_click([MOUSE_BUTTON_MIDDLE], release)

    def buttons_click(self, buttons: List[int], release=True):
        raise_mouse_event(self.dev, buttons, 0, 0, 0, 0)
        self.buttons_state = buttons
        if release:
            self.release()

    def release(self):
        """
        Release Mouse Buttons
        """
        send_mouse_event_identity(self.dev)
        self.buttons_state = MOUSE_BUTTONS_NONE

    def scroll_y(self, position: int):
        """
        scroll in y axis (vertical)
        y should be in range of -127 to 127
        """
        if not -127 <= position <= 127:
            raise RelativeMoveRangeError(
                f"Value of y {position} out of range (-127 - 127)"
            )
        raise_mouse_event(self.dev, self.buttons_state, 0, 0, 0, position)

    def scroll_x(self, position: int):
        """
        scroll in x axis (horizontal)
        x should be in range of -127 to 127
        """
        if not -127 <= position <= 127:
            raise RelativeMoveRangeError(
                f"Value of x: {position} out of range (-127 - 127)"
            )
        raise_mouse_event(self.dev, self.buttons_state, 0, 0, position, 0)

    def raw(self, buttons_state, x, y, scroll_x, scroll_y):
        """
        Control the way you like
        """
        raise_mouse_event(self.dev, buttons_state, x, y, scroll_x, scroll_y)

    def move(self, x, y):
        """
        move the mouse in relative mode
        x,y should be in range of -2047 to 2047
        """
        if not -2047 <= x <= 2047:
            raise RelativeMoveRangeError(f"Value of x: {x} out of range (-2047 - 2047)")
        if not -2047 <= y <= 2047:
            raise RelativeMoveRangeError(f"Value of y: {y} out of range (-2047 - 2047)")
        raise_mouse_event(self.dev, self.buttons_state, x, y, 0, 0)

    def __enter__(self):
        return self

    def _clean_resources(self):
        self.dev.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()

    def close(self):
        self._clean_resources()
