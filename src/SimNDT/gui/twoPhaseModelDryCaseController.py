import numpy as np

from PySide.QtGui import *

from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.ui_twophasemodeldrycase import Ui_twoPhaseModelDryCaseDialog

from SimNDT.core.concreteModel import TwoPhaseModel, Granulometry
from SimNDT.core.geometryObjects import Concrete2Phase


class TwoPhaseModelDryCaseDialog(QDialog, Ui_twoPhaseModelDryCaseDialog):
    def __init__(self, parent=None, scenario=None, SimNDT_ConcreteMicrostructure=None):
        super(TwoPhaseModelDryCaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.scenario = scenario

        self.progressBar.setVisible(False)

        if SimNDT_ConcreteMicrostructure:
            self.fractionDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.Fraction)
            self.labelSpinBox.setValue(SimNDT_ConcreteMicrostructure.LabelAggregate)
            self.minDiameterDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MinDiameter)
            self.maxDiameterDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MaxDiameter)
            self.gradingDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.Grading)
            self.minAspectRatioDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MinAspectRatio)
            self.maxAspectRatioDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MaxAspectRatio)

    def accept(self):

        try:
            fraction = self.fractionDoubleSpinBox.value()
            label = self.labelSpinBox.value()

            minD = self.minDiameterDoubleSpinBox.value() * 1e-3
            maxD = self.maxDiameterDoubleSpinBox.value() * 1e-3

            nG = self.gradingDoubleSpinBox.value()
            minAR = self.minAspectRatioDoubleSpinBox.value()
            maxAR = self.maxAspectRatioDoubleSpinBox.value()


        except:
            msgBox = WarningParms()
            msgBox.exec_()

        MI, NI = np.shape(self.scenario.I)
        Pixel_mm = self.scenario.Pixel_mm

        granulometry = Granulometry(MI, NI, Pixel_mm, minD, maxD, nG, minAR, maxAR, fraction, label)
        twoPhaseModel = TwoPhaseModel(MI, NI, granulometry, self.scenario.Label)
        self.image = twoPhaseModel.compute(self.progressBar)

        self.concrete2PhaseObject = Concrete2Phase(Fraction=fraction, LabelAggregate=label, MinDiameter=minD * 1e3,
                                                   MaxDiameter=maxD * 1e3,
                                                   Grading=nG, MinAspectRatio=minAR, MaxAspectRatio=maxAR)

        QDialog.accept(self)
