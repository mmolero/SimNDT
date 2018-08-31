# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\newscenario.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewModel(object):
    def setupUi(self, NewModel):
        NewModel.setObjectName("NewModel")
        NewModel.setWindowModality(QtCore.Qt.ApplicationModal)
        NewModel.resize(272, 200)
        NewModel.setMinimumSize(QtCore.QSize(272, 200))
        NewModel.setMaximumSize(QtCore.QSize(272, 200))
        NewModel.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newImage.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewModel.setWindowIcon(icon)
        NewModel.setWhatsThis("")
        NewModel.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        NewModel.setSizeGripEnabled(False)
        NewModel.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewModel)
        self.buttonBox.setGeometry(QtCore.QRect(40, 160, 201, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(300, 300))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(NewModel)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 20, 191, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.widthLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName("widthLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widthLabel)
        self.widthLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.widthLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.widthLineEdit.setObjectName("widthLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.widthLineEdit)
        self.heightLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.heightLabel.setObjectName("heightLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.heightLabel)
        self.heightLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.heightLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.heightLineEdit)
        self.pixelLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.pixelLabel.setObjectName("pixelLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.pixelLabel)
        self.pixelLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.pixelLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pixelLineEdit.setObjectName("pixelLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.pixelLineEdit)
        self.labelLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelLabel.setObjectName("labelLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelLabel)
        self.labelSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.labelSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.labelSpinBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.labelSpinBox.setMaximum(240)
        self.labelSpinBox.setSingleStep(40)
        self.labelSpinBox.setObjectName("labelSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.labelSpinBox)

        self.retranslateUi(NewModel)
        self.buttonBox.accepted.connect(NewModel.accept)
        self.buttonBox.rejected.connect(NewModel.reject)
        QtCore.QMetaObject.connectSlotsByName(NewModel)
        NewModel.setTabOrder(self.buttonBox, self.widthLineEdit)
        NewModel.setTabOrder(self.widthLineEdit, self.heightLineEdit)
        NewModel.setTabOrder(self.heightLineEdit, self.pixelLineEdit)
        NewModel.setTabOrder(self.pixelLineEdit, self.labelSpinBox)

    def retranslateUi(self, NewModel):
        _translate = QtCore.QCoreApplication.translate
        NewModel.setWindowTitle(_translate("NewModel", "New Scenario"))
        self.widthLabel.setText(_translate("NewModel", "Width (mm)"))
        self.heightLabel.setText(_translate("NewModel", "Height (mm)"))
        self.pixelLabel.setText(_translate("NewModel", "Pixel/mm"))
        self.labelLabel.setText(_translate("NewModel", "Label"))

import SimNDT.gui.resources_rc

