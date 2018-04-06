__author__ = 'Miguel Molero'



import os
from PySide.QtGui import *

from SimNDT.gui.ui_runsimulation import Ui_runSimulationDialog
from SimNDT.gui.Warnings import WarningParms
import SimNDT.gui.constants as c


class RunSimulation(QDialog, Ui_runSimulationDialog):

    def __init__(self, filename, Simulation, parent=None):

        super(RunSimulation, self).__init__(parent)
        self.setupUi(self)

        self.filename = filename
        self.basename = None
        self.Simulation = Simulation

        self.receiverShow = False
        self.receiverCheckBox.setVisible(False)

        #self.ColormapView = ColorbarWidget()

        self.colormapComboBox.addItems(["jet","gray"])
        self.colormapComboBox.setCurrentIndex(0)
        self.colormapComboBox.setVisible(False)


        self.stepsLabel.setVisible(False)

        self.snapshotStepLabel.setVisible(False)
        self.snapshotStepSpinBox.setVisible(False)


        self.visualizacionRangeLabel.setVisible(False)
        self.visualizacionRangeSpinBox.setVisible(False)

        self.enableSavingFieldsLabel.setVisible(False)
        self.enableSavingFieldsCheckBox.setVisible(False)


        #self.colormapLayout.addWidget(self.ColormapView)



        self.setLayout(self.verticalLayout)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)


        self.viewCheckBox.stateChanged.connect(self.visualizacionRangeSpinBox.setVisible)
        self.viewCheckBox.stateChanged.connect(self.visualizacionRangeLabel.setVisible)
        self.viewCheckBox.stateChanged.connect(self.receiverCheckBox.setVisible)
        self.viewCheckBox.stateChanged.connect(self.colormapComboBox.setVisible)

        self.viewCheckBox.stateChanged.connect(self.receiveFunction)
        self.viewCheckBox.stateChanged.connect(self.updateColor)
        #self.colormapComboBox.activated.connect(self.ColormapView.Show)
        self.snapshotsPushButton.pressed.connect(self.snapshots)
        self.setWindowTitle("Simulation Run Setup")


    def snapshots(self):

        fname = self.filename if self.filename is not None else "."
        fname, filters =  QFileDialog.getSaveFileName(None, "Set Base Name for Snapshots", fname)
        self.basename  = os.path.splitext(fname)[0]

        if self.basename is not None:

            if len(self.basename)!=0:
                self.snapshotStepLabel.setVisible(True)
                self.snapshotStepSpinBox.setVisible(True)

                self.stepsLabel.setVisible(True)
                self.stepsLabel.setText("Simulation Time Steps: %d"%(self.Simulation.TimeSteps))

                self.visualizacionRangeSpinBox.setVisible(True)
                self.visualizacionRangeLabel.setVisible(True)

                self.enableSavingFieldsLabel.setVisible(True)
                self.enableSavingFieldsCheckBox.setVisible(True)

                self.colormapComboBox.setVisible(True)
                self.updateColor()

            else:
                self.basename = None

        else:

            self.basename = None


    def updateColor(self):
        self.colormapComboBox.setCurrentIndex(0)
        #self.ColormapView.Show(0)
        QApplication.processEvents()


    def receiveFunction(self, value):
        self.receiverShow = value


