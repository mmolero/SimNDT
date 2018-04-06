# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generatevideo.ui'
#
# Created: Tue Jun 24 23:40:13 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_generateVideoDialog(object):
    def setupUi(self, generateVideoDialog):
        generateVideoDialog.setObjectName("generateVideoDialog")
        generateVideoDialog.resize(474, 261)
        generateVideoDialog.setMinimumSize(QtCore.QSize(474, 261))
        generateVideoDialog.setMaximumSize(QtCore.QSize(500, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/snapshots.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        generateVideoDialog.setWindowIcon(icon)
        self.widget = QtGui.QWidget(generateVideoDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 461, 241))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addImagesPushButton = QtGui.QPushButton(self.widget)
        self.addImagesPushButton.setObjectName("addImagesPushButton")
        self.verticalLayout.addWidget(self.addImagesPushButton)
        self.listWidget = QtGui.QListWidget(self.widget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videoBasenamePushButton = QtGui.QPushButton(self.widget)
        self.videoBasenamePushButton.setObjectName("videoBasenamePushButton")
        self.horizontalLayout.addWidget(self.videoBasenamePushButton)
        self.videoBasenameLineEdit = QtGui.QLineEdit(self.widget)
        self.videoBasenameLineEdit.setReadOnly(True)
        self.videoBasenameLineEdit.setObjectName("videoBasenameLineEdit")
        self.horizontalLayout.addWidget(self.videoBasenameLineEdit)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.fPSLabel = QtGui.QLabel(self.widget)
        self.fPSLabel.setObjectName("fPSLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.fPSLabel)
        self.fPSSpinBox = QtGui.QSpinBox(self.widget)
        self.fPSSpinBox.setMinimum(1)
        self.fPSSpinBox.setMaximum(30)
        self.fPSSpinBox.setObjectName("fPSSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fPSSpinBox)
        self.horizontalLayout.addLayout(self.formLayout)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(generateVideoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), generateVideoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), generateVideoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(generateVideoDialog)

    def retranslateUi(self, generateVideoDialog):
        generateVideoDialog.setWindowTitle(QtGui.QApplication.translate("generateVideoDialog", "Generate Video ", None, QtGui.QApplication.UnicodeUTF8))
        generateVideoDialog.setToolTip(QtGui.QApplication.translate("generateVideoDialog", "Generate Video from Snapshots", None, QtGui.QApplication.UnicodeUTF8))
        self.addImagesPushButton.setText(QtGui.QApplication.translate("generateVideoDialog", "Add Images", None, QtGui.QApplication.UnicodeUTF8))
        self.videoBasenamePushButton.setText(QtGui.QApplication.translate("generateVideoDialog", "Set Video Name", None, QtGui.QApplication.UnicodeUTF8))
        self.fPSLabel.setText(QtGui.QApplication.translate("generateVideoDialog", "FPS", None, QtGui.QApplication.UnicodeUTF8))


