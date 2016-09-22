# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Ui_Dialog3(object):
    def setupUi(self, Dialog):
        Dialog.setGeometry(520, 240, 300, 200)
        Dialog.setWindowIcon(QtGui.QIcon('crawl.ico'))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(85, 50, 131, 20))
        self.label.setObjectName("label")
        self.pushButton_6 = QtGui.QPushButton(Dialog)
        self.pushButton_6.setGeometry(QtCore.QRect(110, 130, 85, 27))
        self.pushButton_6.setObjectName("pushButton_6")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "MetGeomi", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "AUTHENTICATION FAILED ", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("Dialog", "BACK", None, QtGui.QApplication.UnicodeUTF8))

