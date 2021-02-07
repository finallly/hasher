from .config_handler import configHandler


class fileHandler(object):

    def __init__(self, file, mode):
        self.file = file
        self.mode = mode

    def __enter__(self):
        self.data = open(self.file, mode=self.mode, encoding=configHandler.charset)
        return self.data

    def __exit__(self, *args):
        self.data.close()
