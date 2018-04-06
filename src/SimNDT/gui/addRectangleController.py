__author__ = 'Miguel Molero'



from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_addrectangle import Ui_addRectangleDialog
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.constants import *
import copy


class AddRectangle(QDialog,Ui_addRectangleDialog):

	def __init__(self, parent = None):
		super(AddRectangle,self).__init__(parent)
		self.setupUi(self)
		self.angleLabel.setText("Angle (%s)" % DEGREE_ANGLE)


	def getParms(self):
		return self.centerX, self.centerY, self.width,self.height, self.theta, self.label

	def accept(self):

		try:
			self.centerX = float(self.centerXLineEdit.text())
			self.centerY = float(self.centerYLineEdit.text())
			self.width	= float(self.widthLineEdit.text())
			self.height	= float(self.heightLineEdit.text())
			self.theta	= float(self.angleLineEdit.text())
			self.label = float(self.labelSpinBox.value())

			QDialog.accept(self)

		except:
			msgBox = WarningParms()
			msgBox.exec_()

