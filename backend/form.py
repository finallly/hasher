from PyQt5 import QtWidgets
from PyQt5 import uic
from .consts import Consts


class FormWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(Consts.filename, self)

        # button bindings
        self.buttonEncrypt.clicked.connect(self.encrypt_button)
        self.buttonDecrypt.clicked.connect(self.decrypt_button)

        # keyLine settings
        self.key = str()
        self.hash_field.setReadOnly(True)
        self.keyLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine.editingFinished.connect(self.key_checker)
        self.keyLine.setMaxLength(20)

    def encrypt_button(self):
        pass

    def decrypt_button(self):
        pass

    def key_checker(self) -> None:
        self.key = self.keyLine.text()
