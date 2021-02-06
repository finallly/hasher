import sys
from PyQt5 import QtWidgets

from backend.form import FormWindow
from handlers import configHandler, fileHandler

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    with fileHandler(configHandler.main_css) as file_in:
        application.setStyleSheet(file_in.read())
    window = FormWindow()
    window.show()
    sys.exit(application.exec_())
