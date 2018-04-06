# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'advancedsetupinspections.ui'
#
# Created: Fri May  9 16:20:27 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_advancedSetupDialog(object):
    def setupUi(self, advancedSetupDialog):
        advancedSetupDialog.setObjectName("advancedSetupDialog")
        advancedSetupDialog.resize(273, 204)
        advancedSetupDialog.setMinimumSize(QtCore.QSize(273, 204))
        advancedSetupDialog.setMaximumSize(QtCore.QSize(273, 204))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/simModel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        advancedSetupDialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(advancedSetupDialog)
        self.buttonBox.setGeometry(QtCore.QRect(80, 170, 183, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtGui.QGroupBox(advancedSetupDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 251, 151))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 30, 232, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.backingCheckBox = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.backingCheckBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.backingCheckBox.setObjectName("backingCheckBox")
        self.horizontalLayout.addWidget(self.backingCheckBox)
        self.windowedSourceCheckBox = QtGui.QCheckBox(self.horizontalLayoutWidget)
        self.windowedSourceCheckBox.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.windowedSourceCheckBox.setObjectName("windowedSourceCheckBox")
        self.horizontalLayout.addWidget(self.windowedSourceCheckBox)
        self.waveSourceComboBox = QtGui.QComboBox(self.groupBox)
        self.waveSourceComboBox.setGeometry(QtCore.QRect(10, 80, 231, 26))
        self.waveSourceComboBox.setObjectName("waveSourceComboBox")
        self.waveSourceComboBox.addItem("")
        self.waveSourceComboBox.addItem("")
        self.waveSourceComboBox.addItem("")
        self.sourceTypeComboBox = QtGui.QComboBox(self.groupBox)
        self.sourceTypeComboBox.setGeometry(QtCore.QRect(10, 110, 231, 26))
        self.sourceTypeComboBox.setObjectName("sourceTypeComboBox")
        self.sourceTypeComboBox.addItem("")
        self.sourceTypeComboBox.addItem("")
        self.sourceTypeComboBox.addItem("")

        self.retranslateUi(advancedSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), advancedSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), advancedSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(advancedSetupDialog)

    def retranslateUi(self, advancedSetupDialog):
        advancedSetupDialog.setWindowTitle(QtGui.QApplication.translate("advancedSetupDialog", "Advanced Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("advancedSetupDialog", "Transducer Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.backingCheckBox.setText(QtGui.QApplication.translate("advancedSetupDialog", "PZT Backing", None, QtGui.QApplication.UnicodeUTF8))
        self.windowedSourceCheckBox.setText(QtGui.QApplication.translate("advancedSetupDialog", "Windowed Source", None, QtGui.QApplication.UnicodeUTF8))
        self.waveSourceComboBox.setItemText(0, QtGui.QApplication.translate("advancedSetupDialog", "Longitudinal Wave Source", None, QtGui.QApplication.UnicodeUTF8))
        self.waveSourceComboBox.setItemText(1, QtGui.QApplication.translate("advancedSetupDialog", "Shear Wave Source", None, QtGui.QApplication.UnicodeUTF8))
        self.waveSourceComboBox.setItemText(2, QtGui.QApplication.translate("advancedSetupDialog", "Longitudinal and Shear Wave Sources", None, QtGui.QApplication.UnicodeUTF8))
        self.sourceTypeComboBox.setItemText(0, QtGui.QApplication.translate("advancedSetupDialog", "Pressure", None, QtGui.QApplication.UnicodeUTF8))
        self.sourceTypeComboBox.setItemText(1, QtGui.QApplication.translate("advancedSetupDialog", "Displacement", None, QtGui.QApplication.UnicodeUTF8))
        self.sourceTypeComboBox.setItemText(2, QtGui.QApplication.translate("advancedSetupDialog", "Presure & Displacement", None, QtGui.QApplication.UnicodeUTF8))