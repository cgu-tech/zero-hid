import logging
import threading
import typing
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)

class Error(Exception):
    pass

class WriteError(Error):
    pass

# Create a global thread pool to reuse threads
_thread_pool = ThreadPoolExecutor(max_workers=4)

def _write_to_hid_interface_immediately(hid_file, buffer):
    try:
        hid_file.seek(0)
        hid_file.write(bytearray(buffer))
        hid_file.flush()
    except BlockingIOError:
        logger.error(
            f"Failed to write to HID interface: {hid_file}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q"
        )
        raise

def write_to_hid_interface(hid_file, buffer):
    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug(
            "writing to HID interface %s: %s",
            hid_file,
            " ".join(["0x%02x" % x for x in buffer]),
        )

    # Submit the HID write to the thread pool
    future = _thread_pool.submit(_write_to_hid_interface_immediately, hid_file, buffer)
    try:
        # Wait for at most 0.5 seconds
        future.result(timeout=0.5)
    except FuturesTimeoutError:
        future.cancel()
        raise WriteError(
            f"Timed out writing to HID interface: {hid_file}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q"
        )
    except Exception as e:
        raise WriteError(
            f"Failed to write to HID interface: {hid_file}. Reason: {e}"
        ) from e
