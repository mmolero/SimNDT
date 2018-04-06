__author__ = 'Miguel Molero'

import copy

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_tomographysetup import Ui_tomographySetupDialog

from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.advancedSetupInspectionsController import AdvancedSetupInspections
from SimNDT.gui.signalSetupController import SignalSetup
from SimNDT.gui.previewInspectionsController import PreviewTomography

from SimNDT.core.constants import *
from SimNDT.core.transducer import Transducer
from SimNDT.core.inspectionMethods import Source, Tomography


class TomographySetup(QDialog, Ui_tomographySetupDialog):
    def __init__(self, Scenario, Source, Inspection, Transducers, Signal, parent=None):
        super(TomographySetup, self).__init__(parent)
        self.setupUi(self)

        self.advancedParametersSetupPushButton.pressed.connect(self.advancedSetup)
        self.previewPushButton.pressed.connect(self.preview)
        self.connect(self.pointSourceCheckBox, SIGNAL("stateChanged(int)"), self.pointChanged)
        self.signalSetupPushButton.pressed.connect(self.signalSetup)

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

        if self.Inspection is None or self.Source is None:
            return

        if Inspection.Name == "Tomography":
            self.projectionStepLineEdit.setText(str(Inspection.ProjectionStep))
            self.diameterRingLineEdit.setText(str(Inspection.DiameterRing))
            self.oneProjectionCheckBox.setChecked(bool(Inspection.OneProjection))

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

            if size >= self.Scenario.Width:
                msgBox = WarningParms("Transducer is larger than Scenario Width!!!!")
                if msgBox.exec_():
                    return
            elif size <= 0 and not Point:
                msgBox = WarningParms("Incorrect Transducer Size!!!!")
                if msgBox.exec_():
                    return

            transducer = Transducer('SimNDT-emisor', size, 0, 0, "Top", Point)

            ProjectionStep = float(self.projectionStepLineEdit.text())
            if ProjectionStep > 180 or ProjectionStep <= 0:
                msgBox = WarningParms("Incorrect Projection Angle!!!!")
                if msgBox.exec_():
                    return

            DiameterRing = float(self.diameterRingLineEdit.text())
            if DiameterRing < 0 or DiameterRing >= self.Scenario.Height or DiameterRing >= self.Scenario.Width:
                msgBox = WarningParms("Incorrect Diameter Ring!!!!")
                if msgBox.exec_():
                    return

            OneProjection = self.oneProjectionCheckBox.isChecked()
            tomography = Tomography(ProjectionStep, DiameterRing, OneProjection)

        except:

            msgBox = WarningParms()
            msgBox.exec_()
            return

        dlg = PreviewTomography(tomography, self.Scenario, transducer, self)
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

            transducer = Transducer('SimNDT-emisor', size, 0, 0, "Top", Point, self.window, False, self.backing)
            if self.Transducers is None:
                self.Transducers = list()
                self.Transducers.append(transducer)
            else:
                self.Transducers[0] = transducer

            ProjectionStep = float(self.projectionStepLineEdit.text())
            if ProjectionStep > 180 or ProjectionStep <= 0:
                msgBox = WarningParms("Incorrect Projection Angle!!!!")
                if msgBox.exec_():
                    return

            DiameterRing = float(self.diameterRingLineEdit.text())
            if DiameterRing < 0 or DiameterRing >= self.Scenario.Height or DiameterRing >= self.Scenario.Width:
                msgBox = WarningParms("Incorrect Diameter Ring!!!!")
                if msgBox.exec_():
                    return

            OneProjection = self.oneProjectionCheckBox.isChecked()

            tomography = Tomography(ProjectionStep, DiameterRing, OneProjection)
            self.Inspection = copy.deepcopy(tomography)

            if self.Signal is None:
                msgBox = WarningParms("Please Setup Signal Parameters!!!!")
                if msgBox.exec_():
                    return

        except:
            msgBox = WarningParms()
            msgBox.exec_()
            return

        QDialog.accept(self)
