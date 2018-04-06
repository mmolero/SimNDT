__author__ = 'Miguel Molero'

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_materialsetup import Ui_materialSetupDialog
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.constants import *

from SimNDT.gui.materialLibraryController import MaterialLibrary
import copy
from SimNDT.core.material import Material


class MaterialSetup(QDialog, Ui_materialSetupDialog):
    def __init__(self, SimNDT_Materials, filename=None, parent=None):
        super(MaterialSetup, self).__init__(parent)
        self.setupUi(self)
        self.connectionSetup()
        self.initSetup()

        self.__IsOkAdd = True

        self.SimNDT_Materials = copy.deepcopy(SimNDT_Materials)
        self.filename = filename

        if self.SimNDT_Materials is not None:
            self.__NumMatTmp = len(self.SimNDT_Materials)
            self.updateValues(self.__NumMatTmp)
            self.deleteMaterialPushButton.setEnabled(True)
            # self.materialLibraryPushButton.setEnabled(True)
            self.secondFrame.setEnabled(True)
            self.previousPushButton.setEnabled(True)

        else:
            self.SimNDT_Materials = None
            self.dampingSetup(False)
            self.__NumMatTmp = 0

    def connectionSetup(self):
        self.dampimgCheckBox.stateChanged.connect(self.dampingSetup)
        self.previousPushButton.pressed.connect(self.previous)
        self.nextPushButton.pressed.connect(self.next)
        self.addMaterialPushButton.pressed.connect(self.addMaterial)
        self.deleteMaterialPushButton.pressed.connect(self.deleteMaterial)
        self.applyPushButton.pressed.connect(self.apply)
        self.okPushButton.pressed.connect(self.accept)
        self.cancelPushButton.pressed.connect(self.reject)
        self.materialLibraryPushButton.pressed.connect(self.materialLibrary)

    def initSetup(self):

        self.rhoLabel.setText(RHO_LABEL)
        self.lambdaLabel.setText(LAMBDA_LABEL)
        self.muLabel.setText(MU_LABEL)
        self.etavLabel.setText(ETAV_LABEL)
        self.etasLabel.setText(ETAS_LABEL)
        self.infoLabel.setText("")
        self.dampingSetup(False)

        self.setFocusPolicy(Qt.NoFocus)
        self.previousPushButton.setFocusPolicy(Qt.NoFocus)
        self.nextPushButton.setFocusPolicy(Qt.NoFocus)
        self.deleteMaterialPushButton.setEnabled(False)
        self.materialLibraryPushButton.setEnabled(False)

        self.secondFrame.setEnabled(False)
        self.propertiesFrame.setEnabled(False)
        self.applyPushButton.setEnabled(False)

    def dampingSetup(self, state=False):

        self.etavLabel.setVisible(state)
        self.etasLabel.setVisible(state)
        self.etavLineEdit.setVisible(state)
        self.etasLineEdit.setVisible(state)

    def setValues(self, name, send_values):

        self.rhoLineEdit.setText("%0.2f" % send_values[0])
        self.lambdaLineEdit.setText("%0.2f" % send_values[1])
        self.muLineEdit.setText("%0.2f" % send_values[2])
        self.materialNameLineEdit.setText(name)

        text = """
				      %s = %0.2f
					  <p> %s = %0.2f
			   """ % (VL_LABEL, send_values[3],
                      VT_LABEL, send_values[4])

        self.infoLabel.setText(text)

    def setAllValues(self, name, values):

        self.rhoLineEdit.setText("%0.2f" % values[0])
        self.lambdaLineEdit.setText("%0.2f" % values[1])
        self.muLineEdit.setText("%0.2f" % values[2])
        self.materialNameLineEdit.setText(name)

        text = """
				      %s = %0.2f
					  <p> %s = %0.2f
			   """ % (VL_LABEL, values[3],
                      VT_LABEL, values[4])

        self.infoLabel.setText(text)

        self.labelSpinBox.setValue(values[5])

        self.etavLineEdit.setText("%0.2f" % values[7])
        self.etasLineEdit.setText("%0.2f" % values[8])

    def setClear(self):

        self.rhoLineEdit.clear()
        self.lambdaLineEdit.clear()
        self.muLineEdit.clear()
        self.infoLabel.clear()
        self.etavLineEdit.clear()
        self.etasLineEdit.clear()

    def getAllValues(self):

        name = self.materialNameLineEdit.text()
        rho = float(self.rhoLineEdit.text())
        lam = float(self.lambdaLineEdit.text()) * 1e9
        mu = float(self.muLineEdit.text()) * 1e9
        label = int(self.labelSpinBox.value())
        damping = self.dampimgCheckBox.isChecked()

        try:
            etav = float(self.etavLineEdit.text())
        except:
            etav = 0.0

        try:
            etas = float(self.etasLineEdit.text())
        except:
            etas = 0.0

        values = (rho, lam, mu, label, damping, etav, etas)
        return name, values

    def previous(self):

        if self.SimNDT_Materials is None:
            return

        if len(self.SimNDT_Materials) >= 1:
            self.propertiesFrame.setEnabled(False)

            self.__NumMatTmp -= 1
            if self.__NumMatTmp <= 1:
                self.__NumMatTmp = 1

            self.updateValues(self.__NumMatTmp)
            self.dampimgCheckBox.setChecked(self.SimNDT_Materials[self.__NumMatTmp - 1].Damping)
            if self.SimNDT_Materials[self.__NumMatTmp - 1].Damping:
                self.dampingSetup(True)
            else:
                self.dampingSetup(False)

    def next(self):

        if self.SimNDT_Materials is None:
            return

        if (self.__NumMatTmp + 1) <= len(self.SimNDT_Materials):

            self.__NumMatTmp += 1
            self.propertiesFrame.setEnabled(False)
            self.updateValues(self.__NumMatTmp)

            self.dampimgCheckBox.setChecked(self.SimNDT_Materials[self.__NumMatTmp - 1].Damping)
            if self.SimNDT_Materials[self.__NumMatTmp - 1].Damping:
                self.dampingSetup(True)
            else:
                self.dampingSetup(False)

        if self.__NumMatTmp >= len(self.SimNDT_Materials):
            self.__NumMatTmp = len(self.SimNDT_Materials)

    def updateValues(self, num):

        self.materialNumberlabel.setText(self.tr("Material #%s" % num))

        values = (self.SimNDT_Materials[num - 1].Rho,  # 0
                  self.SimNDT_Materials[num - 1].C12 * 1e-9,  # 1
                  self.SimNDT_Materials[num - 1].C44 * 1e-9,  # 2
                  self.SimNDT_Materials[num - 1].VL,  # 3
                  self.SimNDT_Materials[num - 1].VT,  # 4
                  self.SimNDT_Materials[num - 1].Label,  # 5
                  self.SimNDT_Materials[num - 1].Damping,  # 6
                  self.SimNDT_Materials[num - 1].Eta_v,  # 7
                  self.SimNDT_Materials[num - 1].Eta_s)  # 8

        self.setAllValues(self.SimNDT_Materials[num - 1].Name, values)

        self.dampimgCheckBox.setChecked(self.SimNDT_Materials[num - 1].Damping)
        if self.SimNDT_Materials[num - 1].Damping:
            self.dampingSetup(True)
        else:
            self.dampingSetup(False)

    def addMaterial(self):

        if self.__IsOkAdd:

            self.addMaterialPushButton.setEnabled(False)
            self.__IsOkAdd = False
            self.deleteMaterialPushButton.setEnabled(True)
            self.materialLibraryPushButton.setEnabled(True)
            self.secondFrame.setEnabled(True)
            self.propertiesFrame.setEnabled(True)
            self.applyPushButton.setEnabled(True)
            self.okPushButton.setEnabled(True)

            if self.SimNDT_Materials is None:
                self.previousPushButton.setEnabled(False)
                self.nextPushButton.setEnabled(False)
                self.deleteMaterialPushButton.setEnabled(False)
            elif len(self.SimNDT_Materials) == 1:
                self.previousPushButton.setEnabled(False)
                self.nextPushButton.setEnabled(False)
            else:
                self.previousPushButton.setEnabled(True)
                self.nextPushButton.setEnabled(True)

            if self.SimNDT_Materials is None:
                self.__NumMatTmp = 0
            else:
                self.__NumMatTmp = len(self.SimNDT_Materials)

            self.__NumMatTmp += 1

            self.materialNumberlabel.setText(self.tr("Material #%s" % self.__NumMatTmp))
            self.materialNameLineEdit.clear()
            self.dampimgCheckBox.setChecked(False)

            self.setClear()

    def deleteMaterial(self):

        self.__IsOkAdd = True
        self.okPushButton.setEnabled(True)

        if self.SimNDT_Materials is None:
            self.deleteMaterialPushButton.setEnabled(False)
            return

        if len(self.SimNDT_Materials) >= 1:

            self.__NumMatTmp -= 1
            self.SimNDT_Materials.pop(self.__NumMatTmp)

            if self.__NumMatTmp <= 0:
                self.__NumMatTmp = 0
                self.SimNDT_Materials = None
                self.deleteMaterialPushButton.setEnabled(False)
                self.materialNumberlabel.setText(self.tr("Material #"))
                self.materialNameLineEdit.clear()
                self.dampimgCheckBox.setChecked(False)
                self.setClear()
                self.propertiesFrame.setEnabled(False)

            try:
                self.updateValues(len(self.SimNDT_Materials))
            except:
                pass

            if self.__NumMatTmp <= 1:
                self.addMaterialPushButton.setEnabled(True)
                self.previousPushButton.setEnabled(False)
                self.nextPushButton.setEnabled(False)

            else:
                self.addMaterialPushButton.setEnabled(True)
                self.previousPushButton.setEnabled(True)
                self.nextPushButton.setEnabled(True)

    def apply(self):

        try:
            # if True:
            name, values = self.getAllValues()

            rho = values[0]
            c11 = (values[1] + 2 * values[2])
            c22 = c11
            c12 = values[1]
            c44 = values[2]
            label = values[3]

            damping = values[4]

            if damping:
                eta_v = values[5]
                eta_s = values[6]

            else:
                eta_v = 1e-30
                eta_s = 1e-30

            material = Material(name, rho, c11, c12, c22, c44, label, damping, eta_v, eta_s)

            if self.SimNDT_Materials is None:
                self.SimNDT_Materials = list()
                self.SimNDT_Materials.append(material)
            else:
                N = len(self.SimNDT_Materials)
                if N != 0 and self.__NumMatTmp - 1 < N:
                    self.SimNDT_Materials[self.__NumMatTmp - 1] = material
                else:
                    self.SimNDT_Materials.append(material)

            if self.__NumMatTmp <= 1:
                self.previousPushButton.setEnabled(False)
                self.nextPushButton.setEnabled(False)

            else:
                self.previousPushButton.setEnabled(True)
                self.nextPushButton.setEnabled(True)

            self.deleteMaterialPushButton.setEnabled(True)
            self.addMaterialPushButton.setEnabled(True)
            self.applyPushButton.setEnabled(False)
            self.propertiesFrame.setEnabled(False)
            self.materialLibraryPushButton.setEnabled(False)
            self.__IsOkAdd = True


        except:
            msgBox = WarningParms()
            msgBox.exec_()

    def accept(self):

        if self.__IsOkAdd:
            QDialog.accept(self)

        else:
            msgBox = WarningParms("Please Apply your changes")
            msgBox.exec_()

    def materialLibrary(self):

        dlg = MaterialLibrary(filename=self.filename)
        if dlg.exec_():
            name, values = dlg.getValues()
            send_values = (values[0], values[1] * 1e-9, values[2] * 1e-9, values[3], values[4])
            self.setValues(name, send_values)
