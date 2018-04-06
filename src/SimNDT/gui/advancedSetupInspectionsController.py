__author__ = 'Miguel Molero'



import os, sys
from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_advancedsetupinspections import Ui_advancedSetupDialog
from SimNDT.gui.Warnings import WarningParms


class AdvancedSetupInspections(QDialog, Ui_advancedSetupDialog):

	def __init__(self, Source, Inspection, Transducers, parent=None):
		super(AdvancedSetupInspections,self).__init__(parent)
		self.setupUi(self)


		if Transducers is not None:
			self.windowedSourceCheckBox.setChecked(bool(Transducers[0].Window))
			self.backingCheckBox.setChecked(bool(Transducers[0].PZT))


		if Inspection is None or Source is None:
			return


		if Source.Longitudinal and not Source.Shear:
			self.waveSourceComboBox.setCurrentIndex(0)
		elif not Source.Longitudinal and Source.Shear:
			self.waveSourceComboBox.setCurrentIndex(1)
		elif  Source.Longitudinal and Source.Shear:
			self.waveSourceComboBox.setCurrentIndex(2)
		else:
			self.waveSourceComboBox.setCurrentIndex(0)


		if Source.Pressure and not Source.Displacement:
			self.sourceTypeComboBox.setCurrentIndex(0)
		elif not Source.Pressure and Source.Displacement:
			self.sourceTypeComboBox.setCurrentIndex(1)
		elif  Source.Pressure and Source.Displacement:
			self.sourceTypeComboBox.setCurrentIndex(2)
		else:
			self.sourceTypeComboBox.setCurrentIndex(0)


	def accept(self):

		self.backing = self.backingCheckBox.isChecked()
		self.window  = self.windowedSourceCheckBox.isChecked()
		self.waveSource = self.waveSourceComboBox.currentIndex()
		self.sourceType = self.sourceTypeComboBox.currentIndex()
		QDialog.accept(self)