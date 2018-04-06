__author__ = 'Miguel Molero'

import os, sys
import numpy as np
from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_checksimulation import Ui_checkSimulationDialog
from SimNDT.gui.Warnings import WarningParms
import SimNDT.gui.constants as c


import SimNDT.core.checkSimulation as CheckSim



class CheckSimulation(QDialog, Ui_checkSimulationDialog):

	def __init__(self, Scenario, Materials, Boundaries, Transducers, Inspection, Signal, Simulation, parent = None):
		super(CheckSimulation, self).__init__(parent)
		self.setupUi(self)



		self.closePushButton.pressed.connect(self.close)

		self.treeWidget.clear()
		self.dispatcher = ['Scenario', 'Materials','Boundary','Inspection Method', 'Simulation Setup']

		self.treeWidget.setColumnCount(2)
		self.treeWidget.setHeaderLabels(["Setup","Comments"])
		self.treeWidget.setAlternatingRowColors(True)
		self.treeWidget.header().resizeSection(0, 220)


		self.Boundaries = Boundaries
		self.Scenario   = Scenario
		self.Inspection = Inspection

		self.passAll = False

		scenario_tree = QTreeWidgetItem(self.treeWidget)
		scenario_tree.setText(0,"Scenario")
		scenario_tree.setIcon(0,QIcon(":/mark.png"))


		material_tree = QTreeWidgetItem(self.treeWidget)
		material_tree.setText(0,"Material")
		material_tree.setIcon(0,QIcon(":/mark.png"))


		self.message1 = None
		self.message2 = None
		self.message3 = None
		self.message4 = None
		self.message5 = None

		case = CheckSim.labels(Scenario, Materials)

		if case == 1:
			self.message1 =  "Number of labels in scenario is higher than the number of the defined materials. "

		elif case == 2:
			self.message1 =  "Number of labels in scenario is lower than the number of the defined materials. "


		case = CheckSim.materials(Materials)
		if case == 1:
			self.message2 = "Repeated labels in Materials!!!. "

		case =  CheckSim.isLabelsEquals(Scenario, Materials)
		if case == 1:
			self.message3 =  "Scenario Labels do not coincide with Material Labels!!!. "


		message = ""
		if self.message1 is not None:
			message +=self.message1
			material_tree.setIcon(0,QIcon(":/cross.png"))

		if self.message2 is not None:
			message += self.message2
			material_tree.setIcon(0,QIcon(":/cross.png"))

		if self.message3 is not None:
			message += self.message3
			material_tree.setIcon(0,QIcon(":/cross.png"))

		material_tree.setText(1,message)



		Scenario, Boundaries, isChange = CheckSim.boundariesReLoad(Scenario, Materials,Boundaries, Transducers[0], Inspection, Simulation)


		if isChange:
			self.Boundaries = Boundaries
			self.Scenario = Scenario
			self.message4 = "Found error, but fixed: All boundaries with Air Layers"


		boundary_tree = QTreeWidgetItem(self.treeWidget)
		boundary_tree.setText(0,"Boundaries Conditions")
		boundary_tree.setIcon(0,QIcon(":/mark.png"))

		if self.message4 is not None:
			boundary_tree.setText(1,self.message4)

		self.Inspection.setInspection(Scenario, Transducers[0], Simulation)


		signal_tree = QTreeWidgetItem(self.treeWidget)
		signal_tree.setText(0,"Signal Setup")
		signal_tree.setIcon(0,QIcon(":/mark.png"))

		t = Simulation.t
		try:
			source = Signal.generate(t)
		except Exception as e:
			self.message5 = "Signal does not fit in the Simulation Time, Increase the Simulation Time to solve this issue"
			signal_tree.setText(1,self.message5)
			signal_tree.setIcon(0,QIcon(":/cross.png"))

		if self.message1 is  None and self.message2 is None \
				and self.message3 is None and self.message4 is None\
				and self.message5 is None:
			self.passAll = True



	def close(self):

		if self.passAll:
			QDialog.accept(self)
		else:
			QDialog.reject(self)
