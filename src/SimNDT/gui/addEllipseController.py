__author__ = 'Miguel Molero'


from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_addellipse import Ui_addEllipseDialog
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.constants import *
import copy


class AddEllipse(QDialog,Ui_addEllipseDialog):

	def __init__(self, parent = None):
		super(AddEllipse,self).__init__(parent)
		self.setupUi(self)

		self.angleLabel.setText("Angle (%s)" % DEGREE_ANGLE)


	def getParms(self):
		return self.centerX, self.centerY, self.major,self.minor, self.theta, self.label


	def accept(self):

		try:
			self.centerX = float(self.centerXLineEdit.text())
			self.centerY = float(self.centerYLineEdit.text())
			self.major	= float(self.semiMajorAxisLineEdit.text())
			self.minor	= float(self.semiMinorAxisLineEdit.text())
			self.theta	= float(self.angleLineEdit.text())
			self.label = float(self.labelSpinBox.value())

			QDialog.accept(self)

		except:
			msgBox = WarningParms()
			msgBox.exec_()
