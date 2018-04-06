__author__ = 'Miguel Molero'

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui import resources_rc
from SimNDT.gui.ui_newscenario import Ui_NewModel
from SimNDT.gui.Warnings import WarningParms


class NewScenario(QDialog, Ui_NewModel):
	def __init__(self, parent = None):
		super(NewScenario,self).__init__(parent)
		self.setupUi(self)


	def accept(self):
		try:
			self.width = float(self.widthLineEdit.text())
			self.height = float(self.heightLineEdit.text())
			self.pixel  = float(self.pixelLineEdit.text())
			self.label = int(self.labelSpinBox.value())

		except:
			msgBox = WarningParms()
			msgBox.exec_()
			return

		QDialog.accept(self)



if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	dialog = NewScenario()
	dialog.exec_()
	app.exec_()