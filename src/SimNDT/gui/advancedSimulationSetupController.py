__author__ = 'Miguel Molero'


import os, sys
import numpy as np
from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_advancedsimulationsetup import Ui_advancedSimulationSetupDialog
from SimNDT.gui.Warnings import WarningParms
import SimNDT.gui.constants as c

from SimNDT.core.simulation import Simulation


class AdvancedSimulationSetup(QDialog, Ui_advancedSimulationSetupDialog):

	def __init__(self, SimTime, MaxFreq, Scenario, Materials, Transducers, Simulation, parent=None):
		super(AdvancedSimulationSetup, self).__init__(parent)
		self.setupUi(self)

		self.previewSimulationSetupPushButton.pressed.connect(self.preview)
		self.setMaximumHeight(140)
		self.dtLabel.setText("dt (%ss)"%c.MU)
		self.previewFrame.setVisible(False)

		self.SimTime = SimTime
		self.MaxFreq = MaxFreq
		self.Scenario = Scenario
		self.Materials = Materials
		self.Transducers = Transducers
		self.Simulation = Simulation

		self.dx = None
		self.dt = None

		if self.Simulation is not None:

			timeScale = self.Simulation.TimeScale
			pointCycle = self.Simulation.PointCycle

			self.timeScaleDoubleSpinBox.setValue(timeScale)
			self.pointPerCycleSpinBox.setValue(int(pointCycle))



	def preview(self):

		self.previewFrame.setVisible(True)
		self.setMinimumHeight(300)


		try:
			timeScale = float (self.timeScaleDoubleSpinBox.value())
		except:
			msgBox = WarningParms("Please give correctly the Time Scale")
			if msgBox.exec_():
				return

		try:
			pointCycle = int(self.pointPerCycleSpinBox.value())
		except:
			msgBox = WarningParms("Please give correctly the Points Per Cycles")
			if msgBox.exec_():
				return


		simulation = Simulation(timeScale, self.MaxFreq, pointCycle, self.SimTime, Order=2)

		try:
			simulation.job_parameters(self.Materials, self.Transducers[0])
		except:
			msgBox = WarningParms("Please give correctly the Material Properties")
			if msgBox.exec_():
				return


		simulation.create_numericalModel(self.Scenario)

		self.dxLineEdit.setText("%0.4f"% (simulation.dx * 1e3) )
		self.dtLineEdit.setText("%0.4f"% (simulation.dt * 1e6) )

		M, N = np.shape(self.Scenario.Iabs)
		MM, NN = np.shape(simulation.Im)

		self.geometricSizeLabel.setText("%s x %s"%(M,N))
		self.numericalSizeLabel.setText("%s x %s"%(MM,NN))




	def accept(self):

		try:
			self.TimeScale = float (self.timeScaleDoubleSpinBox.value())
		except:
			msgBox = WarningParms("Please give correctly the Time Scale")
			if msgBox.exec_():
				return

		try:
			self.PointCycle = int(self.pointPerCycleSpinBox.value())
		except:
			msgBox = WarningParms("Please give correctly the Points Per Cycles")
			if msgBox.exec_():
				return

		try:
			self.dx = float ( self.dxLineEdit.text()  ) * 1e-3
		except:
			msgBox = WarningParms("Please give correctly dx !!!!")
			if msgBox.exec_():
				return


		try:
			self.dt = float ( self.dtLineEdit.text()  ) * 1e-6
		except:
			msgBox = WarningParms("Please give correctly dt !!!!")
			if msgBox.exec_():
				return


		QDialog.accept(self)
