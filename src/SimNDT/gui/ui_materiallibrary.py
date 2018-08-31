# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\materiallibrary.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_materialLibraryDialog(object):
    def setupUi(self, materialLibraryDialog):
        materialLibraryDialog.setObjectName("materialLibraryDialog")
        materialLibraryDialog.resize(514, 371)
        materialLibraryDialog.setMinimumSize(QtCore.QSize(514, 371))
        materialLibraryDialog.setMaximumSize(QtCore.QSize(514, 371))
        self.materialListWidget = QtWidgets.QListWidget(materialLibraryDialog)
        self.materialListWidget.setGeometry(QtCore.QRect(20, 20, 221, 331))
        self.materialListWidget.setObjectName("materialListWidget")
        self.frame = QtWidgets.QFrame(materialLibraryDialog)
        self.frame.setGeometry(QtCore.QRect(250, 20, 241, 331))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.materialNameLineEdit = QtWidgets.QLineEdit(self.frame)
        self.materialNameLineEdit.setGeometry(QtCore.QRect(10, 10, 221, 21))
        self.materialNameLineEdit.setObjectName("materialNameLineEdit")
        self.infoLabel = QtWidgets.QLabel(self.frame)
        self.infoLabel.setGeometry(QtCore.QRect(20, 50, 201, 151))
        self.infoLabel.setAutoFillBackground(False)
        self.infoLabel.setObjectName("infoLabel")
        self.okPushButton = QtWidgets.QPushButton(self.frame)
        self.okPushButton.setGeometry(QtCore.QRect(10, 290, 110, 32))
        self.okPushButton.setObjectName("okPushButton")
        self.cancelPushButton = QtWidgets.QPushButton(self.frame)
        self.cancelPushButton.setGeometry(QtCore.QRect(120, 290, 110, 32))
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.createLibraryPushButton = QtWidgets.QPushButton(self.frame)
        self.createLibraryPushButton.setGeometry(QtCore.QRect(10, 220, 221, 32))
        self.createLibraryPushButton.setObjectName("createLibraryPushButton")
        self.createTemplatePushButton = QtWidgets.QPushButton(self.frame)
        self.createTemplatePushButton.setGeometry(QtCore.QRect(10, 250, 221, 32))
        self.createTemplatePushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.createTemplatePushButton.setObjectName("createTemplatePushButton")

        self.retranslateUi(materialLibraryDialog)
        QtCore.QMetaObject.connectSlotsByName(materialLibraryDialog)

    def retranslateUi(self, materialLibraryDialog):
        _translate = QtCore.QCoreApplication.translate
        materialLibraryDialog.setWindowTitle(_translate("materialLibraryDialog", "Material Library"))
        self.materialNameLineEdit.setPlaceholderText(_translate("materialLibraryDialog", "Selected Material"))
        self.infoLabel.setText(_translate("materialLibraryDialog", "Info"))
        self.okPushButton.setText(_translate("materialLibraryDialog", "OK"))
        self.cancelPushButton.setText(_translate("materialLibraryDialog", "Cancel"))
        self.createLibraryPushButton.setText(_translate("materialLibraryDialog", "Load Custom Material Library"))
        self.createTemplatePushButton.setText(_translate("materialLibraryDialog", "Create Library Template"))

