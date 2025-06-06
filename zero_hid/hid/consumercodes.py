# zero_hid/hid/consumercodes.py

from dataclasses import dataclass


@dataclass
class ConsumerCodes:

    def __getitem__(self, key):
        return getattr(self, key)

    KEY_RESERVED = 0x00
    KEY_AC_BACK = 0x01
    KEY_AC_HOME = 0x02

ConsumerCodes = ConsumerCodes()
