# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newscenario.ui'
#
# Created: Tue Jun  3 19:57:36 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

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
        self.buttonBox = QtGui.QDialogButtonBox(NewModel)
        self.buttonBox.setGeometry(QtCore.QRect(40, 160, 201, 32))
        self.buttonBox.setMaximumSize(QtCore.QSize(300, 300))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(NewModel)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 20, 191, 131))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.widthLabel = QtGui.QLabel(self.formLayoutWidget)
        self.widthLabel.setObjectName("widthLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.widthLabel)
        self.widthLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.widthLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.widthLineEdit.setObjectName("widthLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.widthLineEdit)
        self.heightLabel = QtGui.QLabel(self.formLayoutWidget)
        self.heightLabel.setObjectName("heightLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.heightLabel)
        self.heightLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.heightLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.heightLineEdit.setObjectName("heightLineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.heightLineEdit)
        self.pixelLabel = QtGui.QLabel(self.formLayoutWidget)
        self.pixelLabel.setObjectName("pixelLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.pixelLabel)
        self.pixelLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.pixelLineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pixelLineEdit.setObjectName("pixelLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.pixelLineEdit)
        self.labelLabel = QtGui.QLabel(self.formLayoutWidget)
        self.labelLabel.setObjectName("labelLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelLabel)
        self.labelSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.labelSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.labelSpinBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.labelSpinBox.setMaximum(240)
        self.labelSpinBox.setSingleStep(40)
        self.labelSpinBox.setObjectName("labelSpinBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.labelSpinBox)

        self.retranslateUi(NewModel)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewModel.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewModel.reject)
        QtCore.QMetaObject.connectSlotsByName(NewModel)
        NewModel.setTabOrder(self.buttonBox, self.widthLineEdit)
        NewModel.setTabOrder(self.widthLineEdit, self.heightLineEdit)
        NewModel.setTabOrder(self.heightLineEdit, self.pixelLineEdit)
        NewModel.setTabOrder(self.pixelLineEdit, self.labelSpinBox)

    def retranslateUi(self, NewModel):
        NewModel.setWindowTitle(QtGui.QApplication.translate("NewModel", "New Scenario", None, QtGui.QApplication.UnicodeUTF8))
        self.widthLabel.setText(QtGui.QApplication.translate("NewModel", "Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.heightLabel.setText(QtGui.QApplication.translate("NewModel", "Height (mm)", None, QtGui.QApplication.UnicodeUTF8))
        self.pixelLabel.setText(QtGui.QApplication.translate("NewModel", "Pixel/mm", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLabel.setText(QtGui.QApplication.translate("NewModel", "Label", None, QtGui.QApplication.UnicodeUTF8))

