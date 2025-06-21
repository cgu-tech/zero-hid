from zero_hid import Consumer
from zero_hid.hid.consumer import send_consumer_event
from zero_hid.hid.consumercodes import ConsumerCodes
from common import read_bytes, temp_path

# To install tests dependencies:
# source ~/venv/bin/activate && pip install pytest

# To run:
# source ~/venv/bin/activate && cd zero-hid
# sudo chmod 755 run_tests.sh && ./run_tests.sh tests/consumer_test.py

def create_empty_file(dev_path):
    with open(dev_path, "w") as f:
        f.write("")

def send_consumer_event_data(keys):
    with temp_path() as dev_path:
        create_empty_file(dev_path)
        with Device(dev_path) as dev:
            hid_file = dev.get_file()
            send_consumer_event(hid_file, keys)
            hid_file.seek(0)
            data = hid_file.read()
    return data

# Test consumer identity

def test_identity_report():
    data = send_consumer_event_data(None)
    assert data == b"\x03\x00\x00\x00\x00"

# Tests consumer key unique

# return
def test_consumer_ac_back():
    data = send_consumer_event_data([ConsumerCodes.CON_AC_BACK])
    assert data == b"\x03\x24\x02\x00\x00"

# home
def test_consumer_ac_home():
    data = send_consumer_event_data([ConsumerCodes.CON_AC_HOME])
    assert data == b"\x03\x23\x02\x00\x00"

# switch app: LeftAlt (0x04) + Tab (0x2b)

# settings: Application (0x65)

# magnifying glass
def test_consumer_ac_search():
    data = send_consumer_event_data([ConsumerCodes.CON_AC_SEARCH])
    assert data == b"\x03\x21\x02\x00\x00"

# reduce all and show desktop: Left GUI (0x08) + 'd and D' (0x07)

# maximize: Left GUI (0x08) + UpArrow (0x52)

# switch display: Left GUI (0x08) + 'p and P' (0x13)

# musical note
def test_consumer_al_consumer_control_config():
    data = send_consumer_event_data([ConsumerCodes.CON_AL_CONSUMER_CONTROL_CONFIGURATION])
    assert data == b"\x03\x83\x01\x00\x00"

# |<<
def test_consumer_scan_previous_track():
    data = send_consumer_event_data([ConsumerCodes.CON_SCAN_PREVIOUS_TRACK])
    assert data == b"\x03\xb6\x00\x00\x00"

# >||
def test_consumer_play_pause():
    data = send_consumer_event_data([ConsumerCodes.CON_PLAY_PAUSE])
    assert data == b"\x03\xcd\x00\x00\x00"

# >>|
def test_consumer_scan_next_track():
    data = send_consumer_event_data([ConsumerCodes.CON_SCAN_NEXT_TRACK])
    assert data == b"\x03\xb5\x00\x00\x00"

# VOL X
def test_consumer_mute():
    data = send_consumer_event_data([ConsumerCodes.CON_MUTE])
    assert data == b"\x03\xe2\x00\x00\x00"

# VOL -
def test_consumer_volume_decrement():
    data = send_consumer_event_data([ConsumerCodes.CON_VOLUME_DECREMENT])
    assert data == b"\x03\xea\x00\x00\x00"

# VOL +
def test_consumer_volume_increment():
    data = send_consumer_event_data([ConsumerCodes.CON_VOLUME_INCREMENT])
    assert data == b"\x03\xe9\x00\x00\x00"

# Tests consumer key multiple

def test_consumer_volume_decrement_volume_increment():
    data = send_consumer_event_data([ConsumerCodes.CON_VOLUME_DECREMENT, ConsumerCodes.CON_VOLUME_INCREMENT])
    assert data == b"\x03\xea\x00\xe9\x00"
