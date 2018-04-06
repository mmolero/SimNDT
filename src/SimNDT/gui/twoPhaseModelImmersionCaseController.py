import numpy as np

from PySide.QtGui import *

from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.ui_twophasemodelimmersioncase import Ui_twoPhaseModelImmersionCaseDialog

from SimNDT.core.concreteModel import TwoPhaseModel, Granulometry
from SimNDT.core.geometryObjects import Concrete2PhaseImmersion


class TwoPhaseModelImmersionCaseDialog(QDialog, Ui_twoPhaseModelImmersionCaseDialog):
    def __init__(self, parent=None, scenario=None, SimNDT_ConcreteMicrostructure=None):
        super(TwoPhaseModelImmersionCaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.scenario = scenario

        self.progressBar.setVisible(False)

        if SimNDT_ConcreteMicrostructure:
            self.fractionDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.Fraction)
            self.matrixLabelSpinBox.setValue(SimNDT_ConcreteMicrostructure.LabelMatrix)
            self.minDiameterDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MinDiameter)
            self.maxDiameterDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MaxDiameter)
            self.gradingDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.Grading)
            self.minAspectRatioDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MinAspectRatio)
            self.maxAspectRatioDoubleSpinBox.setValue(SimNDT_ConcreteMicrostructure.MaxAspectRatio)

            try:
                self.boxWidthLineEdit.setText(str(SimNDT_ConcreteMicrostructure.BoxWidth))
                self.boxHeightLineEdit.setText(str(SimNDT_ConcreteMicrostructure.BoxHeight))

                self.circularSpecimenCheckBox.setChecked(SimNDT_ConcreteMicrostructure.isCircular)
                self.labelSpinBox.setValue(SimNDT_ConcreteMicrostructure.LabelAggregate)
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


        except:
            msgBox = WarningParms()
            msgBox.exec_()

        MI, NI = np.shape(self.scenario.I)
        Pixel_mm = self.scenario.Pixel_mm
        NC, MC = int(width * Pixel_mm), int(height * Pixel_mm)

        granulometry = Granulometry(MC, NC, Pixel_mm, minD, maxD, nG, minAR, maxAR, fraction, label)
        twoPhaseModel = TwoPhaseModel(MC, NC, granulometry, matrixLabel)
        image = twoPhaseModel.compute(self.progressBar)

        I = np.ones((MI, NI), dtype=np.float32) * self.scenario.Label
        I[MI / 2 - MC / 2:MI / 2 + MC / 2, NI / 2 - NC / 2:NI / 2 + NC / 2] = np.copy(image)

        if isCircular:
            X, Y = np.meshgrid(range(0, NI), range(0, MI))
            Circular = ((X - NI / 2.) ** 2) / ((NC / 2.) ** 2) + ((Y - MI / 2.) ** 2) / ((MC / 2.) ** 2)
            Img = (Circular > 1)
            indx, indy = np.nonzero(Img == 1)
            I[indx, indy] = self.scenario.Label

        self.image = np.copy(I)

        self.concrete2PhaseObjectImmersion = Concrete2PhaseImmersion(Fraction=fraction, LabelMatrix=matrixLabel,
                                                                     MinDiameter=minD * 1e3, MaxDiameter=maxD * 1e3,
                                                                     Grading=nG, MinAspectRatio=minAR,
                                                                     MaxAspectRatio=maxAR,
                                                                     BoxWidth=width, BoxHeight=height,
                                                                     isCircular=isCircular, LabelAggregate=label)

        QDialog.accept(self)
