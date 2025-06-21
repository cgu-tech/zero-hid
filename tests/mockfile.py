from io import BytesIO
import os

class MockFile(BytesIO):
    """
    A mock file object for testing that behaves like a file but ignores seek(0),
    allowing us to capture sequential writes without resetting the file position.
    """

    def seek(self, offset, whence=os.SEEK_SET):
        # Ignore seek(0) only when it's called with SEEK_SET (default)
        if offset == 0 and whence == os.SEEK_SET:
            # Return current position without moving it
            return self.tell()
        return super().seek(offset, whence)

    def tell(self):
        return super().tell()

    def write(self, b):
        return super().write(b)

    def read(self, size=-1):
        return super().read(size)

    def seek_for_test(self, offset, whence=os.SEEK_SET):
        return super().seek(offset, whence)