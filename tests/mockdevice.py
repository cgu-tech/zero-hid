from mockfile import MockFile

class MockDevice:
    def __init__(self):
        self.file = MockFile()

    def get_file(self):
        return self.file

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def close(self):
        pass