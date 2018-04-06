# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checksimulation.ui'
#
# Created: Tue Oct 14 18:32:28 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_checkSimulationDialog(object):
    def setupUi(self, checkSimulationDialog):
        checkSimulationDialog.setObjectName("checkSimulationDialog")
        checkSimulationDialog.resize(620, 220)
        checkSimulationDialog.setMinimumSize(QtCore.QSize(620, 220))
        checkSimulationDialog.setMaximumSize(QtCore.QSize(620, 220))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/check3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        checkSimulationDialog.setWindowIcon(icon)
        self.closePushButton = QtGui.QPushButton(checkSimulationDialog)
        self.closePushButton.setGeometry(QtCore.QRect(10, 180, 110, 32))
        self.closePushButton.setObjectName("closePushButton")
        self.treeWidget = QtGui.QTreeWidget(checkSimulationDialog)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 601, 161))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")

        self.retranslateUi(checkSimulationDialog)
        QtCore.QMetaObject.connectSlotsByName(checkSimulationDialog)

    def retranslateUi(self, checkSimulationDialog):
        checkSimulationDialog.setWindowTitle(QtGui.QApplication.translate("checkSimulationDialog", "Check Simulation Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.closePushButton.setText(QtGui.QApplication.translate("checkSimulationDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

