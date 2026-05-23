from mockfile import MockFile

class MockDevice:
    def __init__(self):
        self._fd = MockFile()

    def get_file_descriptor(self):
        return self._fd

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def close(self):
        pass