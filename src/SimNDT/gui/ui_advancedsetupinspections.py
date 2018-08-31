# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\advancedsetupinspections.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_advancedSetupDialog(object):
    def setupUi(self, advancedSetupDialog):
        advancedSetupDialog.setObjectName("advancedSetupDialog")
        advancedSetupDialog.resize(273, 204)
        advancedSetupDialog.setMinimumSize(QtCore.QSize(273, 204))
        advancedSetupDialog.setMaximumSize(QtCore.QSize(273, 204))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/simModel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        advancedSetupDialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(advancedSetupDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 170, 183, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(advancedSetupDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 251, 151))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 30, 232, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.backingCheckBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.backingCheckBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.backingCheckBox.setObjectName("backingCheckBox")
        self.horizontalLayout.addWidget(self.backingCheckBox)
        self.windowedSourceCheckBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.windowedSourceCheckBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowedSourceCheckBox.setObjectName("windowedSourceCheckBox")
        self.horizontalLayout.addWidget(self.windowedSourceCheckBox)
        self.waveSourceComboBox = QtWidgets.QComboBox(self.groupBox)
        self.waveSourceComboBox.setGeometry(QtCore.QRect(10, 80, 231, 26))
        self.waveSourceComboBox.setObjectName("waveSourceComboBox")
        self.waveSourceComboBox.addItem("")
        self.waveSourceComboBox.addItem("")
        self.waveSourceComboBox.addItem("")
        self.sourceTypeComboBox = QtWidgets.QComboBox(self.groupBox)
        self.sourceTypeComboBox.setGeometry(QtCore.QRect(10, 110, 231, 26))
        self.sourceTypeComboBox.setObjectName("sourceTypeComboBox")
        self.sourceTypeComboBox.addItem("")
        self.sourceTypeComboBox.addItem("")
        self.sourceTypeComboBox.addItem("")

        self.retranslateUi(advancedSetupDialog)
        self.buttonBox.accepted.connect(advancedSetupDialog.accept)
        self.buttonBox.rejected.connect(advancedSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(advancedSetupDialog)

    def retranslateUi(self, advancedSetupDialog):
        _translate = QtCore.QCoreApplication.translate
        advancedSetupDialog.setWindowTitle(_translate("advancedSetupDialog", "Advanced Setup"))
        self.groupBox.setTitle(_translate("advancedSetupDialog", "Transducer Setup"))
        self.backingCheckBox.setText(_translate("advancedSetupDialog", "PZT Backing"))
        self.windowedSourceCheckBox.setText(_translate("advancedSetupDialog", "Windowed Source"))
        self.waveSourceComboBox.setItemText(0, _translate("advancedSetupDialog", "Longitudinal Wave Source"))
        self.waveSourceComboBox.setItemText(1, _translate("advancedSetupDialog", "Shear Wave Source"))
        self.waveSourceComboBox.setItemText(2, _translate("advancedSetupDialog", "Longitudinal and Shear Wave Sources"))
        self.sourceTypeComboBox.setItemText(0, _translate("advancedSetupDialog", "Pressure"))
        self.sourceTypeComboBox.setItemText(1, _translate("advancedSetupDialog", "Displacement"))
        self.sourceTypeComboBox.setItemText(2, _translate("advancedSetupDialog", "Presure & Displacement"))

import SimNDT.gui.resources_rc

