import os
import json
import hashlib

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QCheckBox, QWidget

from backend import CaesarKeyCipher
from handlers import configHandler, fileHandler


class FormWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(configHandler.main_form_file, self)
        self.__local__ = os.getenv('LOCALAPPDATA')
        self.__elements = [self.buttonGet, self.buttonDelete, self.buttonAdd,
                           self.result_field, self.selectAll, self.scrollArea]

        with fileHandler(self.__local__ + configHandler.passwd_source, configHandler.file_in_mode) as file_in:
            __key = json.loads(file_in.read())
            self.local_sha_key = __key.get('key', None)

        if self.local_sha_key is None:
            self.flag = False
            self.keyLine.setPlaceholderText('repeat pass')
        else:
            self.keyLine_2.hide()
            self.flag = True

        for element in self.__elements:
            element.hide()

        # add service form
        self.add_form = addForm(self)

        # button bindings
        self.buttonAdd.clicked.connect(self.button_add)
        self.buttonGet.clicked.connect(self.button_get)
        self.buttonDelete.clicked.connect(self.button_delete)
        self.buttonSubmit.clicked.connect(self.button_submit)

        # keyLine settings
        self.key = str()
        self.keyLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.keyLine.editingFinished.connect(self.key_checker)
        self.keyLine.setMaxLength(30)
        self.keyLine_2.setMaxLength(30)

        # checkboxes setup
        self.selectAll.stateChanged.connect(self.checkbox_all_state_changed)
        self.checkboxes_setup()

        #
        self.label.hide()

    def button_get(self):
        __lst = self.prepare_checkboxes_list()
        self.result_field.clear()
        self.result_field.insertHtml('\n'.join(__lst))

    def button_submit(self):
        if self.flag:
            key_sha = hashlib.sha256(str(self.key).encode(configHandler.charset))
            key_sha = key_sha.hexdigest()

            if key_sha == self.local_sha_key:
                self.buttonSubmit.hide()
                self.keyLine.hide()
                for element in self.__elements:
                    element.show()
        else:
            if self.key == self.keyLine_2.text():
                self.keyLine_2.hide()
                key_sha = hashlib.sha256(str(self.key).encode(configHandler.charset))
                key_sha = key_sha.hexdigest()

                with fileHandler(self.__local__ + configHandler.passwd_source, configHandler.file_out_mode) as file_out:
                    file_out.write(json.dumps({'key': key_sha}))

                self.buttonSubmit.hide()
                self.keyLine.hide()
                self.label.hide()
                for element in self.__elements:
                    element.show()
            else:
                self.label.show()

    def button_delete(self):
        __dict = self._dict
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                text = checkbox.text()
                del __dict[text]

        with fileHandler(self.__local__ + configHandler.data_source, configHandler.file_out_mode) as file_out:
            file_out.write(json.dumps(__dict))

        self.checkboxes_setup()

    def button_add(self):
        self.add_form.show()

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

    def prepare_checkboxes_list(self):
        __dict = self.check_checkboxes()
        __dict = {key: CaesarKeyCipher(value, keyword=self.local_sha_key).decrypt() for key, value in __dict.items()}
        return [f'{key}:\n<div><font color=\"red\">{value}</font></div>' for key, value in __dict.items()]

    # noinspection PyAttributeOutsideInit
    def checkboxes_setup(self):
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)

        with fileHandler(self.__local__ + configHandler.data_source, configHandler.file_in_mode) as file_in:
            layout = QGridLayout()
            self._dict = json.loads(file_in.read())

        self.checkboxes = [QCheckBox(key) for key in self._dict.keys()]

        with fileHandler(configHandler.checkbox_css, configHandler.file_in_mode) as file_in:
            stylesheet = file_in.read()
            for box in self.checkboxes:
                box.setFont(font)
                box.setStyleSheet(stylesheet)
                layout.addWidget(box)

        widget = QWidget()
        widget.setLayout(layout)

        self.scrollArea.setWidget(widget)


class addForm(QtWidgets.QWidget):

    def __init__(self, root):
        super().__init__()
        self.main = root
        uic.loadUi(configHandler.add_form_file, self)

        self.buttonAddRecord.clicked.connect(self.button_add)

    # noinspection PyAttributeOutsideInit
    def button_add(self):
        __dict = {}
        self.service = self.serviceLine.text()
        self.passwd = self.passwdLine.text()
        self.passwd = CaesarKeyCipher(self.passwd, keyword=self.main.local_sha_key).encrypt()

        with fileHandler(self.main.__local__ + configHandler.data_source, configHandler.file_in_mode) as file_in:
            __dict = json.loads(file_in.read())

        __dict[self.service] = self.passwd
        self.serviceLine.clear()
        self.passwdLine.clear()

        with fileHandler(self.main.__local__ + configHandler.data_source, configHandler.file_out_mode) as file_out:
            file_out.write(json.dumps(__dict))

        self.main.checkboxes_setup()
        __lst = self.main.prepare_checkboxes_list()
        self.main.result_field.clear()
        self.main.result_field.insertHtml('\n'.join(__lst))

        self.close()
