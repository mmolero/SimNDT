# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\signalsetup.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignalSetupWidget(object):
    def setupUi(self, SignalSetupWidget):
        SignalSetupWidget.setObjectName("SignalSetupWidget")
        SignalSetupWidget.resize(240, 200)
        SignalSetupWidget.setMinimumSize(QtCore.QSize(240, 200))
        SignalSetupWidget.setMaximumSize(QtCore.QSize(240, 200))
        self.Frame = QtWidgets.QFrame(SignalSetupWidget)
        self.Frame.setGeometry(QtCore.QRect(10, 10, 221, 184))
        self.Frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.Frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Frame.setObjectName("Frame")
        self.gridLayout = QtWidgets.QGridLayout(self.Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.typeComboBox = QtWidgets.QComboBox(self.Frame)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.gridLayout.addWidget(self.typeComboBox, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.amplitudeLabel = QtWidgets.QLabel(self.Frame)
        self.amplitudeLabel.setObjectName("amplitudeLabel")
        self.gridLayout_2.addWidget(self.amplitudeLabel, 0, 0, 1, 1)
        self.amplitudeLineEdit = QtWidgets.QLineEdit(self.Frame)
        self.amplitudeLineEdit.setObjectName("amplitudeLineEdit")
        self.gridLayout_2.addWidget(self.amplitudeLineEdit, 0, 1, 1, 1)
        self.frequencyLabel = QtWidgets.QLabel(self.Frame)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.gridLayout_2.addWidget(self.frequencyLabel, 1, 0, 1, 1)
        self.frequencyLineEdit = QtWidgets.QLineEdit(self.Frame)
        self.frequencyLineEdit.setObjectName("frequencyLineEdit")
        self.gridLayout_2.addWidget(self.frequencyLineEdit, 1, 1, 1, 1)
        self.cyclesLabel = QtWidgets.QLabel(self.Frame)
        self.cyclesLabel.setObjectName("cyclesLabel")
        self.gridLayout_2.addWidget(self.cyclesLabel, 2, 0, 1, 1)
        self.cyclesDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.Frame)
        self.cyclesDoubleSpinBox.setMaximum(20.0)
        self.cyclesDoubleSpinBox.setProperty("value", 1.0)
        self.cyclesDoubleSpinBox.setObjectName("cyclesDoubleSpinBox")
        self.gridLayout_2.addWidget(self.cyclesDoubleSpinBox, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.previewPushButton = QtWidgets.QPushButton(self.Frame)
        self.previewPushButton.setMinimumSize(QtCore.QSize(0, 41))
        self.previewPushButton.setMaximumSize(QtCore.QSize(16777215, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/previewImage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previewPushButton.setIcon(icon)
        self.previewPushButton.setIconSize(QtCore.QSize(24, 24))
        self.previewPushButton.setObjectName("previewPushButton")
        self.gridLayout.addWidget(self.previewPushButton, 2, 0, 1, 1)

        self.retranslateUi(SignalSetupWidget)
        QtCore.QMetaObject.connectSlotsByName(SignalSetupWidget)

    def retranslateUi(self, SignalSetupWidget):
        _translate = QtCore.QCoreApplication.translate
        SignalSetupWidget.setWindowTitle(_translate("SignalSetupWidget", "Form"))
        self.typeComboBox.setItemText(0, _translate("SignalSetupWidget", "Raised Cosine Pulse"))
        self.typeComboBox.setItemText(1, _translate("SignalSetupWidget", "Gaussian Sine Pulse"))
        self.amplitudeLabel.setText(_translate("SignalSetupWidget", "Amplitude"))
        self.frequencyLabel.setText(_translate("SignalSetupWidget", "Frequency (MHz)"))
        self.cyclesLabel.setText(_translate("SignalSetupWidget", "# Cycles"))
        self.previewPushButton.setText(_translate("SignalSetupWidget", "Preview "))

import SimNDT.gui.resources_rc

