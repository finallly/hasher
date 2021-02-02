import json

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QWidget
from PyQt5 import QtGui

from backend import CaesarKeyCipher
from handlers import configHandler, fileHandler


class FormWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(configHandler.ui_file, self)

        # button bindings
        self.buttonAdd.clicked.connect(self.button_get)
        # self.buttonGet.clicked.connect(self.)
        # self.buttonDelete.clicked.connect(self.)

    # keyLine settings
        self.key = str()
        self.result_field.setReadOnly(True)
        self.keyLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine.editingFinished.connect(self.key_checker)
        self.keyLine.setMaxLength(20)

        #
        self.selectAll.stateChanged.connect(self.checkbox_all_state_changed)

        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)

        #
        with fileHandler() as file_in:
            layout = QGridLayout()
            self._dict = json.loads(file_in.read())

        self.checkboxes = [QCheckBox(key) for key in self._dict.keys()]

        for box in self.checkboxes:
            box.setFont(font)
            box.setStyleSheet(configHandler.box_stylesheet)
            layout.addWidget(box)

        widget = QWidget()
        widget.setLayout(layout)

        self.scrollArea.setWidget(widget)

    def button_get(self):
        __dict = self.check_checkboxes()
        #print(CaesarKeyCipher('', keyword=self.key).decrypt())
        __dict = {key: CaesarKeyCipher(value, keyword=self.key).decrypt() for key, value in __dict.items()}
        lst = [f'{key} - {value}' for key, value in __dict.items()]
        self.result_field.setText('\n'.join(lst))

    def decrypt_button(self):
        self.result_field.setText(CaesarKeyCipher(self.data_field.toPlainText(), keyword=self.key).decrypt())

    def key_checker(self) -> None:
        self.key = self.keyLine.text()

    def checkbox_all_state_changed(self, state):
        for checkbox in self.checkboxes:
            checkbox.setCheckState(state)

    def check_checkboxes(self):
        __dict = {}
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                text = checkbox.text()
                __dict[text] = self._dict.get(text)

        return __dict

