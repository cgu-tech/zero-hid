from . import defaults, Device
from .hid.mouse import send_mouse_event, send_mouse_event_identity, MOUSE_BUTTON_LEFT, MOUSE_BUTTON_RIGHT, MOUSE_BUTTON_MIDDLE
from typing import SupportsInt, List
import logging

MOUSE_BUTTONS_NONE   = []  # No mouse buttons

class RelativeMoveRangeError(Exception):
    pass


class Mouse:

    def __init__(self, hid: Device) -> None:
        self.set_hid(hid)
        self.buttons_state = MOUSE_BUTTONS_NONE

    def left_click(self, release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"release:{release}")
        self.buttons_click([MOUSE_BUTTON_LEFT], release)

    def right_click(self, release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"release:{release}")
        self.buttons_click([MOUSE_BUTTON_RIGHT], release)

    def middle_click(self, release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"release:{release}")
        self.buttons_click([MOUSE_BUTTON_MIDDLE], release)

    def buttons_click(self, buttons: List[int], release=True):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"buttons:{buttons},release:{release}")
        send_mouse_event(self.hid_file(), buttons, 0, 0, 0, 0)
        self.buttons_state = buttons
        if release:
            self.release()

    def release(self):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug("Releasing...")
        send_mouse_event_identity(self.hid_file())
        self.buttons_state = MOUSE_BUTTONS_NONE

    def scroll_x(self, position: int):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"buttons:{self.buttons_state},scroll_x:{position}")
        if not -127 <= position <= 127:
            raise RelativeMoveRangeError(
                f"Value of x: {position} out of range (-127 - 127)"
            )
        send_mouse_event(self.hid_file(), self.buttons_state, 0, 0, position, 0)

    def scroll_y(self, position: int):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"buttons:{self.buttons_state},scroll_y:{position}")
        if not -127 <= position <= 127:
            raise RelativeMoveRangeError(
                f"Value of y {position} out of range (-127 - 127)"
            )
        send_mouse_event(self.hid_file(), self.buttons_state, 0, 0, 0, position)

    def raw(self, buttons, x, y, scroll_x, scroll_y):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"buttons:{buttons},x:{x},y:{y},scroll_x:{scroll_x},scroll_y:{scroll_y}")
        send_mouse_event(self.hid_file(), buttons, x, y, scroll_x, scroll_y)
        self.buttons_state = buttons

    def move(self, x, y):
        if logger.getEffectiveLevel() == logging.DEBUG:
            logger.debug(f"buttons:{self.buttons_state},x:{x},y:{y}")
        if not -2047 <= x <= 2047:
            raise RelativeMoveRangeError(f"Value of x: {x} out of range (-2047 - 2047)")
        if not -2047 <= y <= 2047:
            raise RelativeMoveRangeError(f"Value of y: {y} out of range (-2047 - 2047)")
        send_mouse_event(self.hid_file(), self.buttons_state, x, y, 0, 0)

    def set_hid(self, hid: Device):
        self.hid = hid

    def hid_file(self):
        return self.hid.get_file()
