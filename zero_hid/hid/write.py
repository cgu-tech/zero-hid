import errno
import logging
import threading
import typing
import subprocess
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

logger = logging.getLogger(__name__)
USB_HID_SCRIPT_SHELL = "/bin/bash"
USB_HID_SCRIPT_PATH = "/usr/bin/init_usb_gadget"
USB_HID_SCRIPT_RESTART_OPTION = "--restart"

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
                if osEx.errno != errno.EPIPE and osEx.errno != errno.ESHUTDOWN:
                    raise

                if attempt < max_attempts:
                    logger.warning(f"HID broken pipe (attempt {attempt}), reopening...")
                    hid.reopen()
                else:
                    # Try USB HID gadget recovery
                    logger.warning(f"HID broken pipe last attempt reached: reseting USB HID gadget...")
                    logger.warning(f"{USB_HID_SCRIPT_SHELL} {USB_HID_SCRIPT_PATH} {USB_HID_SCRIPT_RESTART_OPTION}")
                    subprocess.run([USB_HID_SCRIPT_SHELL, USB_HID_SCRIPT_PATH, USB_HID_SCRIPT_RESTART_OPTION])
                    logger.warning(f"USB HID reset")
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
    except FuturesTimeoutError as ftEx:
        future.cancel()
        raise WriteError(
            f"Timed out writing to HID interface: {hid_file}. Is USB cable connected and Gadget module installed? check https://git.io/J1T7Q"
        ) from ftEx
    except Exception as ex:
        raise WriteError(
            f"Failed to write to HID interface: {hid_file}. Reason: {ex}"
        ) from ex
