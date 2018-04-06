__author__ = 'Miguel Molero'

import sys
import numpy as np
from PySide.QtGui import *

from SimNDT.gui.ui_simulationsetup import Ui_simulationSetupDialog
from SimNDT.gui.Warnings import WarningParms

from SimNDT.gui.advancedSimulationSetupController import AdvancedSimulationSetup
import SimNDT.gui.constants as c

import SimNDT.engine.infoCL as infoCL
from SimNDT.core.simulation import Simulation

if infoCL.importCL():
    import pyopencl as cl


class SimulationSetup(QDialog, Ui_simulationSetupDialog):
    def __init__(self, Scenario, Materials, Transducers,
                 Signal, Simulation, parent=None):

        super(SimulationSetup, self).__init__(parent)
        self.setupUi(self)

        self.simulationTimeLabel.setText("Simulation Time (%ss)" % c.MU)
        self.advancedSimulationSetupPushButton.pressed.connect(self.advancedSetup)

        font = QFont()
        font.setFamily("Helvetica")
        if sys.platform == "darwin":
            font.setPointSize(12)
        else:
            font.setPointSize(8)
        self.processingDeviceLabel.setFont(font)
        self.deviceComboBox.setFont(font)

        self.timeScale = 1.0
        self.pointCycle = 10
        self.dx_user = None
        self.dt_user = None

        if np.size(Scenario.Iabs) == 1:
            msgBox = WarningParms("Please define the Boundaries Conditions!!!!")
            if msgBox.exec_():
                QDialog.reject(self)

        if infoCL.importCL():
            self.Platforms = infoCL.getPlatforms()
        else:
            self.Platforms = None
            self.deviceComboBox.addItem("CPU [Serial Processing]")
            self.processingDeviceLabel.setText("Processing Devices (Disable OpenCL)")

        if self.Platforms is not None:
            self.PlatformAndDevices = infoCL.getPlatformsAndDevices()
            self.deviceComboBox.clear()

            info = [cl.device_type.to_string(device.type) + ": " + device.name + " OpenCL Platform: " + platform.name
                    for platform, device in self.PlatformAndDevices]
            self.deviceComboBox.addItems(info)
            self.deviceComboBox.addItem("CPU [Serial Processing]")
            self.processingDeviceLabel.setText("Processing Devices (Enable OpenCL)")

        self.Scenario = Scenario
        self.Materials = Materials
        self.Transducers = Transducers
        self.Simulation = Simulation

        if self.Simulation is None:
            self.MaxFreq = 2.0 * Signal.Frequency

        else:
            self.MaxFreq = self.Simulation.MaxFreq
            self.SimTime = self.Simulation.SimulationTime

            if self.Platforms is not None:
                for i, PlatformAndDevice in enumerate(self.PlatformAndDevices):
                    if self.Simulation.Platform == PlatformAndDevice[0].name:
                        if self.Simulation.Device == cl.device_type.to_string(PlatformAndDevice[1].type):
                            print(i, cl.device_type.to_string(PlatformAndDevice[1].type))
                            self.deviceComboBox.setCurrentIndex(i)

            if self.Simulation.Platform == "Serial":
                self.deviceComboBox.setCurrentIndex(self.deviceComboBox.count() - 1)
            self.simulationTimeLineEdit.setText("{0:.4f}".format(self.SimTime * 1e6))
        self.maxFrequencyLineEdit.setText(str(self.MaxFreq * 1e-6))

    def advancedSetup(self):

        try:
            self.MaxFreq = float(self.maxFrequencyLineEdit.text()) * 1e6
        except:
            msgBox = WarningParms("Please give correctly the Maximum Frequency")
            if msgBox.exec_():
                return

        try:
            self.SimTime = float(self.simulationTimeLineEdit.text()) * 1e-6
        except:
            msgBox = WarningParms("Please give correctly the Simulation Time")
            if msgBox.exec_():
                return

        dlg = AdvancedSimulationSetup(self.SimTime, self.MaxFreq,
                                      self.Scenario, self.Materials, self.Transducers, self.Simulation)
        if dlg.exec_():
            self.pointCycle = dlg.PointCycle
            self.timeScale = dlg.TimeScale
            self.dx_user = dlg.dx
            self.dt_user = dlg.dt

    def accept(self):

        try:
            self.MaxFreq = float(self.maxFrequencyLineEdit.text()) * 1e6
        except:
            msgBox = WarningParms("Please give correctly the Maximum Frequency")
            if msgBox.exec_():
                return

        try:
            self.SimTime = float(self.simulationTimeLineEdit.text()) * 1e-6
        except:
            msgBox = WarningParms("Please give correctly the Simulation Time")
            if msgBox.exec_():
                return

        pointCycle = self.pointCycle
        timeScale = self.timeScale

        self.Simulation = Simulation(timeScale, self.MaxFreq, pointCycle, self.SimTime, Order=2)

        try:
            self.Simulation.job_parameters(self.Materials, self.Transducers[0])

        except:
            msgBox = WarningParms("Please give correctly the Material Properties")
            if msgBox.exec_():
                return

        self.Simulation.create_numericalModel(self.Scenario)

        if self.dx_user is not None or self.dt_user is not None:
            self.Simulation.jobByUser(self.dx_user, self.dt_user)
            self.Simulation.create_numericalModel(self.Scenario)

        if self.Platforms is not None:
            if self.deviceComboBox.currentText() == "CPU [Serial Processing]":
                self.Simulation.setPlatform("Serial")
                self.Simulation.setDevice("CPU")
            else:
                PlatformDevice = self.PlatformAndDevices[self.deviceComboBox.currentIndex()]
                self.Simulation.setPlatform(PlatformDevice[0].name)
                self.Simulation.setDevice(cl.device_type.to_string(PlatformDevice[1].type))
                print(PlatformDevice[0].name, cl.device_type.to_string(PlatformDevice[1].type))
        else:
            self.Simulation.setPlatform("Serial")
            self.Simulation.setDevice("CPU")

        QDialog.accept(self)
