import numpy as np

from PySide.QtGui import *

from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.ui_threephasemodeldrycase import Ui_threePhaseModelDryCaseDialog

from SimNDT.core.concreteModel import ThreePhaseModel, Granulometry
from SimNDT.core.geometryObjects import Concrete3Phase


class ThreePhaseModelDryCaseDialog(QDialog, Ui_threePhaseModelDryCaseDialog):
    def __init__(self, parent=None, scenario=None, SimNDT_ConcreteMicrostructure=None):
        super(ThreePhaseModelDryCaseDialog, self).__init__(parent)
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

            self.fractionDoubleSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.FractionAir)
            self.labelSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.LabelAir)
            self.minDiameterDoubleSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.MinDiameterAir)
            self.maxDiameterDoubleSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.MaxDiameterAir)
            self.gradingDoubleSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.GradingAir)

    def accept(self):

        try:
            fraction = self.fractionDoubleSpinBox.value()
            label = self.labelSpinBox.value()

            minD = self.minDiameterDoubleSpinBox.value() * 1e-3
            maxD = self.maxDiameterDoubleSpinBox.value() * 1e-3

            nG = self.gradingDoubleSpinBox.value()
            minAR = self.minAspectRatioDoubleSpinBox.value()
            maxAR = self.maxAspectRatioDoubleSpinBox.value()

            fraction2 = self.fractionDoubleSpinBox_2.value()
            label2 = self.labelSpinBox_2.value()

            minD2 = self.minDiameterDoubleSpinBox_2.value() * 1e-3
            maxD2 = self.maxDiameterDoubleSpinBox_2.value() * 1e-3

            nG2 = self.gradingDoubleSpinBox_2.value()



        except:
            msgBox = WarningParms()
            msgBox.exec_()

        MI, NI = np.shape(self.scenario.I)
        Pixel_mm = self.scenario.Pixel_mm

        granulometry1 = Granulometry(MI, NI, Pixel_mm, minD, maxD, nG, minAR, maxAR, fraction, label)
        granulometry2 = Granulometry(MI, NI, Pixel_mm, minD2, maxD2, nG2, 0, 1, fraction2, label2)
        threePhaseModel = ThreePhaseModel(MI, NI, granulometry1, granulometry2, self.scenario.Label)
        self.image = threePhaseModel.compute(self.progressBar)

        self.concrete3PhaseObject = Concrete3Phase(Fraction=fraction, LabelAggregate=label, MinDiameter=minD * 1e3,
                                                   MaxDiameter=maxD * 1e3,
                                                   Grading=nG, MinAspectRatio=minAR, MaxAspectRatio=maxAR,
                                                   FractionsAir=fraction2, LabelAir=label2, MinDiameterAir=minD2 * 1e3,
                                                   MaxDiameterAir=maxD2 * 1e3, GradingAir=nG2)

        QDialog.accept(self)
