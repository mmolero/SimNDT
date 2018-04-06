# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signalsetup.ui'
#
# Created: Sun Aug 31 16:13:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SignalSetupWidget(object):
    def setupUi(self, SignalSetupWidget):
        SignalSetupWidget.setObjectName("SignalSetupWidget")
        SignalSetupWidget.resize(240, 200)
        SignalSetupWidget.setMinimumSize(QtCore.QSize(240, 200))
        SignalSetupWidget.setMaximumSize(QtCore.QSize(240, 200))
        self.Frame = QtGui.QFrame(SignalSetupWidget)
        self.Frame.setGeometry(QtCore.QRect(10, 10, 221, 184))
        self.Frame.setFrameShape(QtGui.QFrame.Panel)
        self.Frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.Frame.setObjectName("Frame")
        self.gridLayout = QtGui.QGridLayout(self.Frame)
        self.gridLayout.setObjectName("gridLayout")
        self.typeComboBox = QtGui.QComboBox(self.Frame)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.gridLayout.addWidget(self.typeComboBox, 0, 0, 1, 1)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.amplitudeLabel = QtGui.QLabel(self.Frame)
        self.amplitudeLabel.setObjectName("amplitudeLabel")
        self.gridLayout_2.addWidget(self.amplitudeLabel, 0, 0, 1, 1)
        self.amplitudeLineEdit = QtGui.QLineEdit(self.Frame)
        self.amplitudeLineEdit.setObjectName("amplitudeLineEdit")
        self.gridLayout_2.addWidget(self.amplitudeLineEdit, 0, 1, 1, 1)
        self.frequencyLabel = QtGui.QLabel(self.Frame)
        self.frequencyLabel.setObjectName("frequencyLabel")
        self.gridLayout_2.addWidget(self.frequencyLabel, 1, 0, 1, 1)
        self.frequencyLineEdit = QtGui.QLineEdit(self.Frame)
        self.frequencyLineEdit.setObjectName("frequencyLineEdit")
        self.gridLayout_2.addWidget(self.frequencyLineEdit, 1, 1, 1, 1)
        self.cyclesLabel = QtGui.QLabel(self.Frame)
        self.cyclesLabel.setObjectName("cyclesLabel")
        self.gridLayout_2.addWidget(self.cyclesLabel, 2, 0, 1, 1)
        self.cyclesDoubleSpinBox = QtGui.QDoubleSpinBox(self.Frame)
        self.cyclesDoubleSpinBox.setMaximum(20.0)
        self.cyclesDoubleSpinBox.setProperty("value", 1.0)
        self.cyclesDoubleSpinBox.setObjectName("cyclesDoubleSpinBox")
        self.gridLayout_2.addWidget(self.cyclesDoubleSpinBox, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.previewPushButton = QtGui.QPushButton(self.Frame)
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
        SignalSetupWidget.setWindowTitle(QtGui.QApplication.translate("SignalSetupWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtGui.QApplication.translate("SignalSetupWidget", "Raised Cosine Pulse", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtGui.QApplication.translate("SignalSetupWidget", "Gaussian Sine Pulse", None, QtGui.QApplication.UnicodeUTF8))
        self.amplitudeLabel.setText(QtGui.QApplication.translate("SignalSetupWidget", "Amplitude", None, QtGui.QApplication.UnicodeUTF8))
        self.frequencyLabel.setText(QtGui.QApplication.translate("SignalSetupWidget", "Frequency (MHz)", None, QtGui.QApplication.UnicodeUTF8))
        self.cyclesLabel.setText(QtGui.QApplication.translate("SignalSetupWidget", "# Cycles", None, QtGui.QApplication.UnicodeUTF8))
        self.previewPushButton.setText(QtGui.QApplication.translate("SignalSetupWidget", "Preview ", None, QtGui.QApplication.UnicodeUTF8))
