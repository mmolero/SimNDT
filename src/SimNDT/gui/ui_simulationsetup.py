# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\simulationsetup.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_simulationSetupDialog(object):
    def setupUi(self, simulationSetupDialog):
        simulationSetupDialog.setObjectName("simulationSetupDialog")
        simulationSetupDialog.resize(280, 235)
        simulationSetupDialog.setMinimumSize(QtCore.QSize(280, 235))
        simulationSetupDialog.setMaximumSize(QtCore.QSize(280, 235))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/simModel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        simulationSetupDialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(simulationSetupDialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 200, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtWidgets.QFrame(simulationSetupDialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 256, 181))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.simulationTimeLabel = QtWidgets.QLabel(self.frame)
        self.simulationTimeLabel.setObjectName("simulationTimeLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.simulationTimeLabel)
        self.simulationTimeLineEdit = QtWidgets.QLineEdit(self.frame)
        self.simulationTimeLineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.simulationTimeLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.simulationTimeLineEdit.setObjectName("simulationTimeLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.simulationTimeLineEdit)
        self.maxFrequencyLabel = QtWidgets.QLabel(self.frame)
        self.maxFrequencyLabel.setObjectName("maxFrequencyLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.maxFrequencyLabel)
        self.maxFrequencyLineEdit = QtWidgets.QLineEdit(self.frame)
        self.maxFrequencyLineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.maxFrequencyLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.maxFrequencyLineEdit.setObjectName("maxFrequencyLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.maxFrequencyLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.advancedSimulationSetupPushButton = QtWidgets.QPushButton(self.frame)
        self.advancedSimulationSetupPushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.advancedSimulationSetupPushButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.advancedSimulationSetupPushButton.setIcon(icon)
        self.advancedSimulationSetupPushButton.setIconSize(QtCore.QSize(24, 24))
        self.advancedSimulationSetupPushButton.setObjectName("advancedSimulationSetupPushButton")
        self.verticalLayout.addWidget(self.advancedSimulationSetupPushButton)
        self.processingDeviceLabel = QtWidgets.QLabel(self.frame)
        self.processingDeviceLabel.setObjectName("processingDeviceLabel")
        self.verticalLayout.addWidget(self.processingDeviceLabel)
        self.deviceComboBox = QtWidgets.QComboBox(self.frame)
        self.deviceComboBox.setObjectName("deviceComboBox")
        self.verticalLayout.addWidget(self.deviceComboBox)

        self.retranslateUi(simulationSetupDialog)
        self.buttonBox.accepted.connect(simulationSetupDialog.accept)
        self.buttonBox.rejected.connect(simulationSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(simulationSetupDialog)

    def retranslateUi(self, simulationSetupDialog):
        _translate = QtCore.QCoreApplication.translate
        simulationSetupDialog.setWindowTitle(_translate("simulationSetupDialog", "Simulation Setup"))
        self.simulationTimeLabel.setText(_translate("simulationSetupDialog", "Simulation Time"))
        self.maxFrequencyLabel.setText(_translate("simulationSetupDialog", "Max Frequency (MHz)"))
        self.advancedSimulationSetupPushButton.setText(_translate("simulationSetupDialog", "Advanced Simulation Setup"))
        self.processingDeviceLabel.setText(_translate("simulationSetupDialog", "Processing Device"))

import SimNDT.gui.resources_rc
