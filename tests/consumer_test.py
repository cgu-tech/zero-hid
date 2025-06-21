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

def test_consumer_volume_decrement():
    data = send_consumer_event_data([ConsumerCodes.CON_VOLUME_DECREMENT], None)
    assert data == b"\x03\xea\x00\x00\x00"

def test_consumer_volume_decrement_volume_increment():
    data = send_consumer_event_data([ConsumerCodes.CON_VOLUME_DECREMENT, ConsumerCodes.CON_VOLUME_INCREMENT], None)
    assert data == b"\x03\xea\x00\xe9\x00"
