# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\checksimulation.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_checkSimulationDialog(object):
    def setupUi(self, checkSimulationDialog):
        checkSimulationDialog.setObjectName("checkSimulationDialog")
        checkSimulationDialog.resize(700, 220)
        checkSimulationDialog.setMinimumSize(QtCore.QSize(700, 220))
        checkSimulationDialog.setMaximumSize(QtCore.QSize(700, 220))
        checkSimulationDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/check3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        checkSimulationDialog.setWindowIcon(icon)
        self.closePushButton = QtWidgets.QPushButton(checkSimulationDialog)
        self.closePushButton.setGeometry(QtCore.QRect(10, 180, 110, 32))
        self.closePushButton.setObjectName("closePushButton")
        self.treeWidget = QtWidgets.QTreeWidget(checkSimulationDialog)
        self.treeWidget.setGeometry(QtCore.QRect(10, 10, 681, 161))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")

        self.retranslateUi(checkSimulationDialog)
        QtCore.QMetaObject.connectSlotsByName(checkSimulationDialog)

    def retranslateUi(self, checkSimulationDialog):
        _translate = QtCore.QCoreApplication.translate
        checkSimulationDialog.setWindowTitle(_translate("checkSimulationDialog", "Check Simulation Setup"))
        self.closePushButton.setText(_translate("checkSimulationDialog", "Close"))

import SimNDT.gui.resources_rc

