# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulationsetup.ui'
#
# Created: Sun Jul 20 21:15:19 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_simulationSetupDialog(object):
    def setupUi(self, simulationSetupDialog):
        simulationSetupDialog.setObjectName("simulationSetupDialog")
        simulationSetupDialog.resize(280, 235)
        simulationSetupDialog.setMinimumSize(QtCore.QSize(280, 235))
        simulationSetupDialog.setMaximumSize(QtCore.QSize(280, 235))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/simModel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        simulationSetupDialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(simulationSetupDialog)
        self.buttonBox.setGeometry(QtCore.QRect(60, 200, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame = QtGui.QFrame(simulationSetupDialog)
        self.frame.setGeometry(QtCore.QRect(10, 10, 256, 181))
        self.frame.setFrameShape(QtGui.QFrame.Panel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.simulationTimeLabel = QtGui.QLabel(self.frame)
        self.simulationTimeLabel.setObjectName("simulationTimeLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.simulationTimeLabel)
        self.simulationTimeLineEdit = QtGui.QLineEdit(self.frame)
        self.simulationTimeLineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.simulationTimeLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.simulationTimeLineEdit.setObjectName("simulationTimeLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.simulationTimeLineEdit)
        self.maxFrequencyLabel = QtGui.QLabel(self.frame)
        self.maxFrequencyLabel.setObjectName("maxFrequencyLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.maxFrequencyLabel)
        self.maxFrequencyLineEdit = QtGui.QLineEdit(self.frame)
        self.maxFrequencyLineEdit.setMinimumSize(QtCore.QSize(80, 0))
        self.maxFrequencyLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.maxFrequencyLineEdit.setObjectName("maxFrequencyLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.maxFrequencyLineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.advancedSimulationSetupPushButton = QtGui.QPushButton(self.frame)
        self.advancedSimulationSetupPushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.advancedSimulationSetupPushButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.advancedSimulationSetupPushButton.setIcon(icon)
        self.advancedSimulationSetupPushButton.setIconSize(QtCore.QSize(24, 24))
        self.advancedSimulationSetupPushButton.setObjectName("advancedSimulationSetupPushButton")
        self.verticalLayout.addWidget(self.advancedSimulationSetupPushButton)
        self.processingDeviceLabel = QtGui.QLabel(self.frame)
        self.processingDeviceLabel.setObjectName("processingDeviceLabel")
        self.verticalLayout.addWidget(self.processingDeviceLabel)
        self.deviceComboBox = QtGui.QComboBox(self.frame)
        self.deviceComboBox.setObjectName("deviceComboBox")
        self.verticalLayout.addWidget(self.deviceComboBox)

        self.retranslateUi(simulationSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), simulationSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), simulationSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(simulationSetupDialog)

    def retranslateUi(self, simulationSetupDialog):
        simulationSetupDialog.setWindowTitle(QtGui.QApplication.translate("simulationSetupDialog", "Simulation Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.simulationTimeLabel.setText(QtGui.QApplication.translate("simulationSetupDialog", "Simulation Time", None, QtGui.QApplication.UnicodeUTF8))
        self.maxFrequencyLabel.setText(QtGui.QApplication.translate("simulationSetupDialog", "Max Frequency (MHz)", None, QtGui.QApplication.UnicodeUTF8))
        self.advancedSimulationSetupPushButton.setText(QtGui.QApplication.translate("simulationSetupDialog", "Advanced Simulation Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.processingDeviceLabel.setText(QtGui.QApplication.translate("simulationSetupDialog", "Processing Device", None, QtGui.QApplication.UnicodeUTF8))

