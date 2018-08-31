# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\generatevideo.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_generateVideoDialog(object):
    def setupUi(self, generateVideoDialog):
        generateVideoDialog.setObjectName("generateVideoDialog")
        generateVideoDialog.resize(474, 261)
        generateVideoDialog.setMinimumSize(QtCore.QSize(474, 261))
        generateVideoDialog.setMaximumSize(QtCore.QSize(500, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/snapshots.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        generateVideoDialog.setWindowIcon(icon)
        self.widget = QtWidgets.QWidget(generateVideoDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 461, 241))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addImagesPushButton = QtWidgets.QPushButton(self.widget)
        self.addImagesPushButton.setObjectName("addImagesPushButton")
        self.verticalLayout.addWidget(self.addImagesPushButton)
        self.listWidget = QtWidgets.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videoBasenamePushButton = QtWidgets.QPushButton(self.widget)
        self.videoBasenamePushButton.setObjectName("videoBasenamePushButton")
        self.horizontalLayout.addWidget(self.videoBasenamePushButton)
        self.videoBasenameLineEdit = QtWidgets.QLineEdit(self.widget)
        self.videoBasenameLineEdit.setReadOnly(True)
        self.videoBasenameLineEdit.setObjectName("videoBasenameLineEdit")
        self.horizontalLayout.addWidget(self.videoBasenameLineEdit)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.fPSLabel = QtWidgets.QLabel(self.widget)
        self.fPSLabel.setObjectName("fPSLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fPSLabel)
        self.fPSSpinBox = QtWidgets.QSpinBox(self.widget)
        self.fPSSpinBox.setMinimum(1)
        self.fPSSpinBox.setMaximum(30)
        self.fPSSpinBox.setObjectName("fPSSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fPSSpinBox)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(generateVideoDialog)
        self.buttonBox.accepted.connect(generateVideoDialog.accept)
        self.buttonBox.rejected.connect(generateVideoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(generateVideoDialog)

    def retranslateUi(self, generateVideoDialog):
        _translate = QtCore.QCoreApplication.translate
        generateVideoDialog.setWindowTitle(_translate("generateVideoDialog", "Generate Video "))
        generateVideoDialog.setToolTip(_translate("generateVideoDialog", "Generate Video from Snapshots"))
        self.addImagesPushButton.setText(_translate("generateVideoDialog", "Add Images"))
        self.videoBasenamePushButton.setText(_translate("generateVideoDialog", "Set Video Name"))
        self.fPSLabel.setText(_translate("generateVideoDialog", "FPS"))

import SimNDT.gui.resources_rc

