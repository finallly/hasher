# import sys
# from PyQt5 import QtWidgets
#
# from backend.form import FormWindow
#
#
# if __name__ == '__main__':
#     application = QtWidgets.QApplication(sys.argv)
#     window = FormWindow()
#     window.show()
#     sys.exit(application.exec_())
import json


with open('E:\data\_passwords.json', mode='r', encoding='utf8') as fin:
    _dict = json.loads(fin.read())
    print(_dict)