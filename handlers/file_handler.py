from .config_handler import configHandler


class fileHandler(object):

    def __init__(self):
        self.file = configHandler.data_source

    def __enter__(self):
        self.data = open(self.file, mode=configHandler.file_mode, encoding=configHandler.charset)
        return self.data

    def __exit__(self, *args):
        self.data.close()
