# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'threephasemodelimmersioncase.ui'
#
# Created: Thu Dec  4 20:20:28 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_threePhaseModelImmersionCaseDialog(object):
    def setupUi(self, threePhaseModelImmersionCaseDialog):
        threePhaseModelImmersionCaseDialog.setObjectName("threePhaseModelImmersionCaseDialog")
        threePhaseModelImmersionCaseDialog.resize(473, 576)
        threePhaseModelImmersionCaseDialog.setMaximumSize(QtCore.QSize(473, 576))
        self.buttonBox = QtGui.QDialogButtonBox(threePhaseModelImmersionCaseDialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 540, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.progressBar = QtGui.QProgressBar(threePhaseModelImmersionCaseDialog)
        self.progressBar.setGeometry(QtCore.QRect(30, 510, 411, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.groupBox = QtGui.QGroupBox(threePhaseModelImmersionCaseDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 451, 221))
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.groupBox.setFlat(True)
        self.groupBox.setObjectName("groupBox")
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setGeometry(QtCore.QRect(10, 30, 441, 181))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayoutWidget = QtGui.QWidget(self.frame)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 419, 162))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gradingDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.gradingDoubleSpinBox.setMinimum(0.01)
        self.gradingDoubleSpinBox.setMaximum(0.8)
        self.gradingDoubleSpinBox.setSingleStep(0.2)
        self.gradingDoubleSpinBox.setProperty("value", 0.1)
        self.gradingDoubleSpinBox.setObjectName("gradingDoubleSpinBox")
        self.gridLayout.addWidget(self.gradingDoubleSpinBox, 2, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.labelSpinBox = QtGui.QSpinBox(self.gridLayoutWidget)
        self.labelSpinBox.setMaximum(240)
        self.labelSpinBox.setSingleStep(40)
        self.labelSpinBox.setProperty("value", 80)
        self.labelSpinBox.setObjectName("labelSpinBox")
        self.gridLayout.addWidget(self.labelSpinBox, 1, 0, 1, 1)
        self.minAspectRatioDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.minAspectRatioDoubleSpinBox.setMinimum(0.2)
        self.minAspectRatioDoubleSpinBox.setMaximum(1.0)
        self.minAspectRatioDoubleSpinBox.setProperty("value", 0.5)
        self.minAspectRatioDoubleSpinBox.setObjectName("minAspectRatioDoubleSpinBox")
        self.gridLayout.addWidget(self.minAspectRatioDoubleSpinBox, 3, 2, 1, 1)
        self.minDiameterDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.minDiameterDoubleSpinBox.setMinimum(0.2)
        self.minDiameterDoubleSpinBox.setMaximum(20.0)
        self.minDiameterDoubleSpinBox.setSingleStep(0.1)
        self.minDiameterDoubleSpinBox.setProperty("value", 0.5)
        self.minDiameterDoubleSpinBox.setObjectName("minDiameterDoubleSpinBox")
        self.gridLayout.addWidget(self.minDiameterDoubleSpinBox, 0, 2, 1, 1)
        self.fractionLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.fractionLabel.setObjectName("fractionLabel")
        self.gridLayout.addWidget(self.fractionLabel, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.fractionDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.fractionDoubleSpinBox.setMinimum(0.1)
        self.fractionDoubleSpinBox.setMaximum(70.0)
        self.fractionDoubleSpinBox.setProperty("value", 10.0)
        self.fractionDoubleSpinBox.setObjectName("fractionDoubleSpinBox")
        self.gridLayout.addWidget(self.fractionDoubleSpinBox, 0, 0, 1, 1)
        self.maxDiameterDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.maxDiameterDoubleSpinBox.setMinimum(0.02)
        self.maxDiameterDoubleSpinBox.setMaximum(20.0)
        self.maxDiameterDoubleSpinBox.setSingleStep(0.1)
        self.maxDiameterDoubleSpinBox.setProperty("value", 10.0)
        self.maxDiameterDoubleSpinBox.setObjectName("maxDiameterDoubleSpinBox")
        self.gridLayout.addWidget(self.maxDiameterDoubleSpinBox, 1, 2, 1, 1)
        self.maxAspectRatioDoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.maxAspectRatioDoubleSpinBox.setMinimum(0.3)
        self.maxAspectRatioDoubleSpinBox.setMaximum(1.0)
        self.maxAspectRatioDoubleSpinBox.setSingleStep(0.1)
        self.maxAspectRatioDoubleSpinBox.setProperty("value", 0.8)
        self.maxAspectRatioDoubleSpinBox.setObjectName("maxAspectRatioDoubleSpinBox")
        self.gridLayout.addWidget(self.maxAspectRatioDoubleSpinBox, 4, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 4, 3, 1, 1)
        self.labelLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.labelLabel.setObjectName("labelLabel")
        self.gridLayout.addWidget(self.labelLabel, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 3, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(threePhaseModelImmersionCaseDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 340, 451, 171))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.frame_2 = QtGui.QFrame(self.groupBox_2)
        self.frame_2.setGeometry(QtCore.QRect(10, 30, 441, 131))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.gridLayoutWidget_2 = QtGui.QWidget(self.frame_2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 419, 111))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.fractionDoubleSpinBox_2 = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.fractionDoubleSpinBox_2.setMinimum(0.1)
        self.fractionDoubleSpinBox_2.setMaximum(10.0)
        self.fractionDoubleSpinBox_2.setProperty("value", 1.0)
        self.fractionDoubleSpinBox_2.setObjectName("fractionDoubleSpinBox_2")
        self.gridLayout_2.addWidget(self.fractionDoubleSpinBox_2, 0, 0, 1, 1)
        self.gradingDoubleSpinBox_2 = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.gradingDoubleSpinBox_2.setMinimum(0.01)
        self.gradingDoubleSpinBox_2.setMaximum(0.8)
        self.gradingDoubleSpinBox_2.setSingleStep(0.2)
        self.gradingDoubleSpinBox_2.setProperty("value", 0.1)
        self.gradingDoubleSpinBox_2.setObjectName("gradingDoubleSpinBox_2")
        self.gridLayout_2.addWidget(self.gradingDoubleSpinBox_2, 2, 2, 1, 1)
        self.labelLabel_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.labelLabel_2.setObjectName("labelLabel_2")
        self.gridLayout_2.addWidget(self.labelLabel_2, 1, 1, 1, 1)
        self.labelSpinBox_2 = QtGui.QSpinBox(self.gridLayoutWidget_2)
        self.labelSpinBox_2.setMaximum(240)
        self.labelSpinBox_2.setSingleStep(40)
        self.labelSpinBox_2.setProperty("value", 120)
        self.labelSpinBox_2.setObjectName("labelSpinBox_2")
        self.gridLayout_2.addWidget(self.labelSpinBox_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.minDiameterDoubleSpinBox_2 = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.minDiameterDoubleSpinBox_2.setMinimum(0.2)
        self.minDiameterDoubleSpinBox_2.setMaximum(20.0)
        self.minDiameterDoubleSpinBox_2.setSingleStep(0.1)
        self.minDiameterDoubleSpinBox_2.setProperty("value", 0.5)
        self.minDiameterDoubleSpinBox_2.setObjectName("minDiameterDoubleSpinBox_2")
        self.gridLayout_2.addWidget(self.minDiameterDoubleSpinBox_2, 0, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 3, 1, 1)
        self.maxDiameterDoubleSpinBox_2 = QtGui.QDoubleSpinBox(self.gridLayoutWidget_2)
        self.maxDiameterDoubleSpinBox_2.setMinimum(0.02)
        self.maxDiameterDoubleSpinBox_2.setMaximum(20.0)
        self.maxDiameterDoubleSpinBox_2.setSingleStep(0.1)
        self.maxDiameterDoubleSpinBox_2.setProperty("value", 1.0)
        self.maxDiameterDoubleSpinBox_2.setObjectName("maxDiameterDoubleSpinBox_2")
        self.gridLayout_2.addWidget(self.maxDiameterDoubleSpinBox_2, 1, 2, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 3, 1, 1)
        self.fractionLabel_2 = QtGui.QLabel(self.gridLayoutWidget_2)
        self.fractionLabel_2.setObjectName("fractionLabel_2")
        self.gridLayout_2.addWidget(self.fractionLabel_2, 0, 1, 1, 1)
        self.frame_3 = QtGui.QFrame(threePhaseModelImmersionCaseDialog)
        self.frame_3.setGeometry(QtCore.QRect(10, 10, 451, 91))
        self.frame_3.setFrameShape(QtGui.QFrame.Panel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.gridLayoutWidget_3 = QtGui.QWidget(self.frame_3)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 10, 411, 71))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)
        self.boxWidthLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.boxWidthLineEdit.setObjectName("boxWidthLineEdit")
        self.gridLayout_3.addWidget(self.boxWidthLineEdit, 0, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 3, 1, 1)
        self.boxHeightLineEdit = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.boxHeightLineEdit.setObjectName("boxHeightLineEdit")
        self.gridLayout_3.addWidget(self.boxHeightLineEdit, 0, 2, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 1, 1, 1)
        self.circularSpecimenCheckBox = QtGui.QCheckBox(self.gridLayoutWidget_3)
        self.circularSpecimenCheckBox.setObjectName("circularSpecimenCheckBox")
        self.gridLayout_3.addWidget(self.circularSpecimenCheckBox, 1, 2, 1, 2)
        self.matrixLabelSpinBox = QtGui.QSpinBox(self.gridLayoutWidget_3)
        self.matrixLabelSpinBox.setMaximum(240)
        self.matrixLabelSpinBox.setSingleStep(40)
        self.matrixLabelSpinBox.setProperty("value", 40)
        self.matrixLabelSpinBox.setObjectName("matrixLabelSpinBox")
        self.gridLayout_3.addWidget(self.matrixLabelSpinBox, 1, 0, 1, 1)

        self.retranslateUi(threePhaseModelImmersionCaseDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), threePhaseModelImmersionCaseDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), threePhaseModelImmersionCaseDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(threePhaseModelImmersionCaseDialog)

    def retranslateUi(self, threePhaseModelImmersionCaseDialog):
        threePhaseModelImmersionCaseDialog.setWindowTitle(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Three-Phase Model (Immersion Case)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Aggregates", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Grading Curve Coeff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Max Diameter (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.fractionLabel.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Concentration (%)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Min Diameter (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.fractionDoubleSpinBox.setSuffix(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Max Aspect Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLabel.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Min Aspect Ratio", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Air Voids", None, QtGui.QApplication.UnicodeUTF8))
        self.fractionDoubleSpinBox_2.setSuffix(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLabel_2.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Min Diameter (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Grading Curve Coeff", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Max Diameter (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.fractionLabel_2.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Concentration (%)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Box Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Box Height (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Cement Matrix Label", None, QtGui.QApplication.UnicodeUTF8))
        self.circularSpecimenCheckBox.setText(QtGui.QApplication.translate("threePhaseModelImmersionCaseDialog", "Circular Specimen", None, QtGui.QApplication.UnicodeUTF8))

