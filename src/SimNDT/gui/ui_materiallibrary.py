# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'materiallibrary.ui'
#
# Created: Sat Apr 19 12:47:47 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_materialLibraryDialog(object):
    def setupUi(self, materialLibraryDialog):
        materialLibraryDialog.setObjectName("materialLibraryDialog")
        materialLibraryDialog.resize(514, 371)
        materialLibraryDialog.setMinimumSize(QtCore.QSize(514, 371))
        materialLibraryDialog.setMaximumSize(QtCore.QSize(514, 371))
        self.materialListWidget = QtGui.QListWidget(materialLibraryDialog)
        self.materialListWidget.setGeometry(QtCore.QRect(20, 20, 221, 331))
        self.materialListWidget.setObjectName("materialListWidget")
        self.frame = QtGui.QFrame(materialLibraryDialog)
        self.frame.setGeometry(QtCore.QRect(250, 20, 241, 331))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.materialNameLineEdit = QtGui.QLineEdit(self.frame)
        self.materialNameLineEdit.setGeometry(QtCore.QRect(10, 10, 221, 21))
        self.materialNameLineEdit.setObjectName("materialNameLineEdit")
        self.infoLabel = QtGui.QLabel(self.frame)
        self.infoLabel.setGeometry(QtCore.QRect(20, 50, 201, 151))
        self.infoLabel.setAutoFillBackground(False)
        self.infoLabel.setObjectName("infoLabel")
        self.okPushButton = QtGui.QPushButton(self.frame)
        self.okPushButton.setGeometry(QtCore.QRect(10, 290, 110, 32))
        self.okPushButton.setObjectName("okPushButton")
        self.cancelPushButton = QtGui.QPushButton(self.frame)
        self.cancelPushButton.setGeometry(QtCore.QRect(120, 290, 110, 32))
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.createLibraryPushButton = QtGui.QPushButton(self.frame)
        self.createLibraryPushButton.setGeometry(QtCore.QRect(10, 220, 221, 32))
        self.createLibraryPushButton.setObjectName("createLibraryPushButton")
        self.createTemplatePushButton = QtGui.QPushButton(self.frame)
        self.createTemplatePushButton.setGeometry(QtCore.QRect(10, 250, 221, 32))
        self.createTemplatePushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.createTemplatePushButton.setObjectName("createTemplatePushButton")

        self.retranslateUi(materialLibraryDialog)
        QtCore.QMetaObject.connectSlotsByName(materialLibraryDialog)

    def retranslateUi(self, materialLibraryDialog):
        materialLibraryDialog.setWindowTitle(QtGui.QApplication.translate("materialLibraryDialog", "Material Library", None, QtGui.QApplication.UnicodeUTF8))
        self.materialNameLineEdit.setPlaceholderText(QtGui.QApplication.translate("materialLibraryDialog", "Selected Material", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("materialLibraryDialog", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.okPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.createLibraryPushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Load Custom Material Library", None, QtGui.QApplication.UnicodeUTF8))
        self.createTemplatePushButton.setText(QtGui.QApplication.translate("materialLibraryDialog", "Create Library Template", None, QtGui.QApplication.UnicodeUTF8))

