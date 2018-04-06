import numpy as np

from PySide.QtGui import *

from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.ui_threephasemodelimmersioncase import Ui_threePhaseModelImmersionCaseDialog

from SimNDT.core.concreteModel import ThreePhaseModel, Granulometry
from SimNDT.core.geometryObjects import Concrete3PhaseImmersion


class ThreePhaseModelImmersionCaseDialog(QDialog, Ui_threePhaseModelImmersionCaseDialog):
    def __init__(self, parent=None, scenario=None, SimNDT_ConcreteMicrostructure=None):
        super(ThreePhaseModelImmersionCaseDialog, self).__init__(parent)
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

            try:
                self.boxWidthLineEdit.setText(str(SimNDT_ConcreteMicrostructure.BoxWidth))
                self.boxHeightLineEdit.setText(str(SimNDT_ConcreteMicrostructure.BoxHeight))

                self.circularSpecimenCheckBox.setChecked(SimNDT_ConcreteMicrostructure.isCircular)
                self.labelSpinBox_2.setValue(SimNDT_ConcreteMicrostructure.LabelAir)
            except:
                pass

    def accept(self):

        try:

            width = float(self.boxWidthLineEdit.text())
            height = float(self.boxHeightLineEdit.text())
            matrixLabel = self.matrixLabelSpinBox.value()
            isCircular = self.circularSpecimenCheckBox.isChecked()

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
        NC, MC = int(width * Pixel_mm), int(height * Pixel_mm)

        granulometry = Granulometry(MC, NC, Pixel_mm, minD, maxD, nG, minAR, maxAR, fraction, label)
        granulometry2 = Granulometry(MC, NC, Pixel_mm, minD2, maxD2, nG2, 0, 1, fraction2, label2)
        threePhaseModel = ThreePhaseModel(MC, NC, granulometry, granulometry2, matrixLabel)
        image = threePhaseModel.compute(self.progressBar)

        I = np.ones((MI, NI), dtype=np.float32) * self.scenario.Label
        I[MI / 2 - MC / 2:MI / 2 + MC / 2, NI / 2 - NC / 2:NI / 2 + NC / 2] = np.copy(image)

        if isCircular:
            X, Y = np.meshgrid(range(0, NI), range(0, MI))
            Circular = ((X - NI / 2.) ** 2) / ((NC / 2.) ** 2) + ((Y - MI / 2.) ** 2) / ((MC / 2.) ** 2)
            Img = (Circular > 1)
            indx, indy = np.nonzero(Img == 1)
            I[indx, indy] = self.scenario.Label

        self.image = np.copy(I)

        self.concrete3PhaseObjectImmersion = Concrete3PhaseImmersion(Fraction=fraction, LabelAggregate=label,
                                                                     MinDiameter=minD * 1e3, MaxDiameter=maxD * 1e3,
                                                                     Grading=nG, MinAspectRatio=minAR,
                                                                     MaxAspectRatio=maxAR,
                                                                     FractionsAir=fraction2, LabelAir=label2,
                                                                     MinDiameterAir=minD2 * 1e3,
                                                                     MaxDiameterAir=maxD2 * 1e3, GradingAir=nG2,
                                                                     BoxWidth=width, BoxHeight=height,
                                                                     isCircular=isCircular)

        QDialog.accept(self)
