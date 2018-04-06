__author__ = 'Miguel'

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_singlelaunchsetup import Ui_singleLaunchSetupDialog
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.advancedSetupInspectionsController import AdvancedSetupInspections
from SimNDT.gui.previewInspectionsController import PreviewSingleLaunch
from SimNDT.gui.signalSetupController import SignalSetup

import numpy as np

from SimNDT.core.constants import *
from SimNDT.core.transducer import Transducer
from SimNDT.core.inspectionMethods import Transmission, PulseEcho, Source

import copy


class SingleLaunchSetup(QDialog, Ui_singleLaunchSetupDialog):
    def __init__(self, Scenario, Source, Inspection, Transducers, Signal, parent=None):
        super(SingleLaunchSetup, self).__init__(parent)
        self.setupUi(self)

        self.advancedParametersSetupPushButton.pressed.connect(self.advancedSetup)
        self.previewPushButton.pressed.connect(self.preview)
        self.connect(self.pointSourceCheckBox, SIGNAL("stateChanged(int)"), self.pointChanged)
        self.signalSetupPushButton.pressed.connect(self.signalSetup)

        self.locationComboBox.setEnabled(False)
        self.transmissionRadioButton.setChecked(True)

        self.backing = False
        self.window = False
        self.sourceType = 0
        self.waveSource = 0

        self.Scenario = Scenario
        self.Source = Source
        self.Inspection = Inspection
        self.Transducers = Transducers
        self.Signal = Signal

        if self.Transducers is not None:
            item = self.Transducers[0]
            self.pointSourceCheckBox.setChecked(bool(item.PointSource))
            if not bool(item.PointSource):
                self.transducerSizeLineEdit.setText(str(item.Size))
            self.centerOffsetLineEdit.setText(str(item.CenterOffset))
            self.borderOffsetLineEdit.setText(str(item.BorderOffset))

        else:
            self.centerOffsetLineEdit.setText(str(0))
            self.borderOffsetLineEdit.setText(str(0))

        if self.Inspection is None or self.Source is None:
            return

        if Inspection.Name == "Transmission" or Inspection.Name == "PulseEcho":
            if Inspection.Name == "Transmission":
                self.transmissionRadioButton.setChecked(True)
            else:
                self.pulseEchoRadioButton.setChecked(True)

    def pointChanged(self, state):

        self.transducerSizeLineEdit.setEnabled(not state)
        self.transducerSizeLineEdit.setVisible(not state)
        self.transducerSizeLabel.setEnabled(not state)
        self.transducerSizeLabel.setVisible(not state)
        if state:
            self.transducerSizeLineEdit.setText("")

    def advancedSetup(self):

        dlg = AdvancedSetupInspections(self.Source, self.Inspection, self.Transducers)
        if dlg.exec_():
            self.backing = dlg.backing
            self.window = dlg.window
            self.sourceType = dlg.sourceType
            self.waveSource = dlg.waveSource

    def preview(self):

        try:

            location = self.locationComboBox.currentText()
            Point = self.pointSourceCheckBox.isChecked()

            try:
                if Point:
                    size = 0
                else:
                    size = float(self.transducerSizeLineEdit.text())
            except:
                msgBox = WarningParms("Give correctly the transducer Size")
                if msgBox.exec_():
                    return

            centerOffset = float(self.centerOffsetLineEdit.text())
            borderOffset = float(self.borderOffsetLineEdit.text())

            if size >= self.Scenario.Width:
                msgBox = WarningParms("Transducer is larger than Scenario Width!!!!")
                if msgBox.exec_():
                    return
            elif size <= 0 and not Point:
                msgBox = WarningParms("Incorrect Transducer Size!!!!")
                if msgBox.exec_():
                    return

            if (np.abs(centerOffset) + size / 2.0 >= self.Scenario.Width / 2.0):
                msgBox = WarningParms("Transducer is out of Scenario!!!!")
                if msgBox.exec_():
                    return

            if borderOffset < 0 or borderOffset >= self.Scenario.Height:
                msgBox = WarningParms("Transducer is out of Scenario!!!!")
                if msgBox.exec_():
                    return

            transducer = Transducer('SimNDT-emisor', size, centerOffset, borderOffset, location, Point)
            method = Transmission(location) if self.transmissionRadioButton.isChecked() else PulseEcho(location)


        except:

            msgBox = WarningParms()
            msgBox.exec_()
            return

        dlg = PreviewSingleLaunch(method, self.Scenario, transducer, self)
        dlg.show()

    def signalSetup(self):

        dlg = SignalSetup(self.Signal, self)
        if dlg.exec_():
            self.Signal = copy.deepcopy(dlg.Signal)

    def accept(self):

        try:

            if self.Source is None:
                self.Source = Source()

            if self.waveSource == WaveSource.Longitudinal:
                self.Source.Longitudinal = True
                self.Source.Shear = False
            elif self.waveSource == WaveSource.Shear:
                self.Source.Longitudinal = False
                self.Source.Shear = True
            elif self.waveSource == WaveSource.LongitudinalAndShear:
                self.Source.Longitudinal = True
                self.Source.Shear = True
            else:
                self.Source.Longitudinal = True
                self.Source.Shear = False

            if self.sourceType == TypeSource.Pressure:
                self.Source.Pressure = True
                self.Source.Displacement = False
            elif self.sourceType == TypeSource.Displacement:
                self.Source.Pressure = False
                self.Source.Displacement = True
            elif self.sourceType == TypeSource.PressureAndDisplacement:
                self.Source.Pressure = True
                self.Source.Displacement = True
            else:
                self.Source.Pressure = True
                self.Source.Displacement = False

            location = self.locationComboBox.currentText()
            Point = self.pointSourceCheckBox.isChecked()

            try:

                if Point:
                    size = 0
                else:
                    size = float(self.transducerSizeLineEdit.text())

            except:
                msgBox = WarningParms("Give correctly the transducer Size")
                if msgBox.exec_():
                    return

            centerOffset = float(self.centerOffsetLineEdit.text())
            borderOffset = float(self.borderOffsetLineEdit.text())

            if size >= self.Scenario.Width:
                msgBox = WarningParms("Transducer is larger than Scenario Width!!!!")
                if msgBox.exec_():
                    return
            elif size <= 0 and not Point:
                msgBox = WarningParms("Incorrect Transducer Size!!!!")
                if msgBox.exec_():
                    return

            if (np.abs(centerOffset) + size / 2.0 >= self.Scenario.Width / 2.0):
                msgBox = WarningParms("Transducer is out of Scenario!!!!")
                if msgBox.exec_():
                    return

            if borderOffset < 0 or borderOffset >= self.Scenario.Height:
                msgBox = WarningParms("Transducer is out of Scenario!!!!")
                if msgBox.exec_():
                    return

            transducer = Transducer('SimNDT-emisor', size, centerOffset, borderOffset, location, Point, self.window,
                                    False, self.backing)
            if self.Transducers is None:
                self.Transducers = list()
                self.Transducers.append(transducer)
            else:
                self.Transducers[0] = transducer

            self.Inspection = Transmission(location) if self.transmissionRadioButton.isChecked() else PulseEcho(
                location)

            if self.Signal is None:
                msgBox = WarningParms("Please Setup Signal Parameters!!!!")
                if msgBox.exec_():
                    return



        except:

            msgBox = WarningParms()
            msgBox.exec_()
            return

        QDialog.accept(self)
