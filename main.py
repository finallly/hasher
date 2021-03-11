import os
import sys
from PyQt5 import QtWidgets

from backend.form import FormWindow
from handlers import configHandler, fileHandler

__local__ = os.getenv('LOCALAPPDATA')

try:
    os.mkdir(__local__ + configHandler.key_storage)
except FileExistsError:
    pass
try:
    with fileHandler(__local__ + configHandler.data_source, mode=configHandler.file_create_mode) as file_in:
        file_in.write(str(dict()))
except FileExistsError:
    pass
try:
    with fileHandler(__local__ + configHandler.passwd_source, mode=configHandler.file_create_mode) as file_in:
        file_in.write(str(dict()))
except FileExistsError:
    pass

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    with fileHandler(configHandler.main_qss, configHandler.file_in_mode) as file_in:
        application.setStyleSheet(file_in.read())
    window = FormWindow()
    window.show()
    sys.exit(application.exec_())
