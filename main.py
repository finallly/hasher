import sys
from PyQt5 import QtWidgets

from backend.form import FormWindow
from handlers import configHandler

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    application.setStyleSheet(configHandler.stylesheet)
    window = FormWindow()
    window.show()
    sys.exit(application.exec_())
