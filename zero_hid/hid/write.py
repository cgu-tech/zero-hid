import logging
import threading
import typing
import errno
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)

class Error(Exception):
    pass

class WriteError(Error):
    pass

# Create a global thread pool to reuse threads
_thread_pool = ThreadPoolExecutor(max_workers=4)
_write_lock = threading.Lock()

def _write_to_hid_interface_immediately(hid, buffer):
    with _write_lock:
        hid_file = hid.get_file_descriptor()
        max_retries = 2
        max_attempts = max_retries - 1
        bytes = bytearray(buffer)
        for attempt in range(max_retries):
            try:
                hid_file.seek(0)
                hid_file.write(bytes)
                hid_file.flush()
                return

            except BlockingIOError:
                logger.error(
                    f"Failed to write to HID interface: {hid_file}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q"
                )
                raise

            except OSError as osEx:
                if osEx.errno != errno.EPIPE and osEx.errno != 108:
                    raise

                if attempt < max_attempts:
                    logger.warning(f"HID broken pipe (attempt {attempt}), reopening...")
                    hid.reopen()
                else:
                    raise

def write_to_hid_interface(hid, buffer):
    hid_file = hid.get_file_descriptor()
    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug("writing to HID interface %s: %s...", hid_file, " ".join(["0x%02x" % x for x in buffer]))

    # Submit the HID write to the thread pool
    future = _thread_pool.submit(_write_to_hid_interface_immediately, hid, buffer)
    try:
        # Wait for at most 0.5 seconds
        future.result(timeout=0.5)
    except FuturesTimeoutError:
        future.cancel()
        raise WriteError(
            f"Timed out writing to HID interface: {hid_file}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q"
        )
    except Exception as ex:
        raise WriteError(
            f"Failed to write to HID interface: {hid_file}. Reason: {ex}"
        ) from ex
