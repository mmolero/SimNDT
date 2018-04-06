__author__ = 'Miguel Molero'




import sys
from PySide.QtCore import *
from PySide.QtGui	import *


class WarningParms(QMessageBox):

	def __init__(self, message="Please fill all parameters",  parent=None):

		super(WarningParms,self).__init__(parent)
		self.setText(self.tr(message))
		self.setWindowModality(Qt.WindowModal)
		self.setIcon(QMessageBox.Warning)
		#On Top
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


class DoneParms(QMessageBox):

	def __init__(self, message="Done!!!!!!",  parent=None):

		super(DoneParms,self).__init__(parent)
		self.setText(self.tr(message))
		self.setWindowModality(Qt.WindowModal)
		self.setIcon(QMessageBox.Information)
		#On Top
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)