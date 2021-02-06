from .config_handler import configHandler


class fileHandler(object):

    def __init__(self, file):
        self.file = file

    def __enter__(self):
        self.data = open(self.file, mode=configHandler.file_mode, encoding=configHandler.charset)
        return self.data

    def __exit__(self, *args):
        self.data.close()
