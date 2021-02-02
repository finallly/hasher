from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5 import QtCore

from backend import Consts
from backend import CaesarKeyCipher


class FormWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(Consts.ui_file, self)

        # button bindings
        self.buttonEncrypt.clicked.connect(self.encrypt_button)
        self.buttonDecrypt.clicked.connect(self.decrypt_button)

        # keyLine settings
        self.key = str()
        self.result_field.setReadOnly(True)
        self.keyLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine.editingFinished.connect(self.key_checker)
        self.keyLine.setMaxLength(20)

    def encrypt_button(self):
        self.result_field.setText(CaesarKeyCipher(self.data_field.toPlainText(), keyword=self.key).encrypt())

    def decrypt_button(self):
        self.result_field.setText(CaesarKeyCipher(self.data_field.toPlainText(), keyword=self.key).decrypt())

    def key_checker(self) -> None:
        self.key = self.keyLine.text()
