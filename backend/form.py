import json
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QWidget

from backend import CaesarKeyCipher
from handlers import configHandler, fileHandler


class FormWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(configHandler.ui_file, self)

        # button bindings
        # self.buttonAdd.clicked.connect(self.)
        self.buttonGet.clicked.connect(self.button_get)
        self.buttonDelete.clicked.connect(self.button_delete)

        # keyLine settings
        self.key = str()
        self.result_field.setReadOnly(True)
        self.keyLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine.editingFinished.connect(self.key_checker)
        self.keyLine.setMaxLength(49)

        # checkboxes setup
        self.selectAll.stateChanged.connect(self.checkbox_all_state_changed)
        self.checkboxes_setup()

    def button_get(self):
        __dict = self.check_checkboxes()
        __dict = {key: CaesarKeyCipher(value, keyword=self.key).decrypt() for key, value in __dict.items()}
        lst = [f'{key}:\n<div><font color=\"red\">{value}</font></div>' for key, value in __dict.items()]
        self.result_field.clear()
        self.result_field.insertHtml('\n'.join(lst))

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

    def button_delete(self):
        __dict = self._dict
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                text = checkbox.text()
                del __dict[text]

        with fileHandler(configHandler.data_source) as file_in:
            file_in.write(json.dumps(__dict))

        self.checkboxes_setup()

    # noinspection PyAttributeOutsideInit
    def checkboxes_setup(self):
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)

        with fileHandler(configHandler.data_source) as file_in:
            layout = QGridLayout()
            self._dict = json.loads(file_in.read())

        self.checkboxes = [QCheckBox(key) for key in self._dict.keys()]

        for box in self.checkboxes:
            box.setFont(font)
            with fileHandler(configHandler.checkbox_css) as file_in:
                box.setStyleSheet(file_in.read())
            layout.addWidget(box)

        widget = QWidget()
        widget.setLayout(layout)

        self.scrollArea.setWidget(widget)
