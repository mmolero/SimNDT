__author__ = 'Miguel Molero'

import os, sys
from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_materiallibrary import Ui_materialLibraryDialog
from SimNDT.gui.constants import *
from SimNDT.core.materialLibrary import getMaterialLibrary, CC


class MaterialLibrary(QDialog, Ui_materialLibraryDialog):
    def __init__(self, filename=None, parent=None):
        super(MaterialLibrary, self).__init__(parent)
        self.setupUi(self)
        self.connectionSetup()

        self.filename = filename
        self.Library = getMaterialLibrary()
        self.materialListWidget.addItems(list(self.Library.keys()))

    def connectionSetup(self):

        self.connect(self.materialListWidget, SIGNAL("itemSelectionChanged()"), self.selectedMaterial)
        self.connect(self.materialListWidget, SIGNAL("itemDoubleClicked(QListWidgetItem *)"), self.accept)
        self.createTemplatePushButton.pressed.connect(self.createTemplate)
        self.createLibraryPushButton.pressed.connect(self.createLibrary)

        self.okPushButton.pressed.connect(self.accept)
        self.cancelPushButton.pressed.connect(self.reject)

    def selectedMaterial(self):

        self.key = self.materialListWidget.currentItem().text()
        self.values = self.Library[self.key]

        self.materialNameLineEdit.setText(self.key)

        text = """     %s = %0.2f
					  <p> %s = %0.2f
					  <p> %s = %0.2f
					  <p> %s = %0.2f
					  <p> %s = %0.2f
			   """ % (RHO_LABEL, self.values[0],
                      LAMBDA_LABEL, self.values[1] * 1e-9,
                      MU_LABEL, self.values[2] * 1e-9,
                      VL_LABEL, self.values[3],
                      VT_LABEL, self.values[4])

        self.infoLabel.setText(text)

    def getValues(self):
        return self.key, self.values

    def createTemplate(self):

        fname = self.filename if self.filename is not None else "."
        formats = ["*.%s" % "txt"]
        fname, filters = QFileDialog.getSaveFileName(None, "Create Template Material Library (.txt)", fname,
                                                     "sim Files (%s)" % " ".join(formats))

        if fname:
            with open(fname, 'w') as f:
                f.write("#Do not edit this section\n")
                f.write("#\n")
                f.write("#Define Materials in each row using the following format:\n")
                f.write("#\n")
                f.write("#Name, Rho VL, VT\n")
                f.write("#\n")
                f.write("#where Rho=Density, VL= longitudinal Velocity, VT=Shear Velocity\n")
                f.write("#\n")
                f.write("#example:\n")
                f.write("#\n")
                f.write("#Water, 1000, 1480, 0.0\n")
                f.write("#\n")
                f.write("#\n")
                f.write("#Change the below examples with your own materials\n")
                f.write("#\n")
                f.write("#\n")
                f.write("#\n")
                f.write("Material 1, 1000, 1480, 0\n")
                f.write("artificial, 2000, 1400, 800\n")

    def createLibrary(self):

        dir = os.path.dirname(self.filename) if self.filename is not None else "."
        formats = ["*.%s" % "txt"]
        fname, filters = QFileDialog.getOpenFileName(None, "Open Custom Material Library (.txt)", dir,
                                                     "txt Files (%s)" % " ".join(formats))

        if fname:

            newMaterials = []

            with open(fname, 'r') as f:
                for line in f:

                    if line.startswith("#"):
                        pass

                    elif len(line) <= 3:
                        pass

                    elif len(line.strip().split(',')) == 4:
                        elem = line.strip().split(',')
                        if len(elem) == 4:
                            newMaterials.append(CC([elem[0], (float(elem[1]), float(elem[2]), float(elem[3]))]))

            if len(newMaterials) != 0:

                count = len(self.Library)
                newCount = len(newMaterials)

                for item in newMaterials:
                    self.Library[item[0]] = item[1]
                    self.materialListWidget.clear()
                    self.materialListWidget.addItems(list(self.Library.keys()))

                for i in range(count, count + newCount):
                    self.materialListWidget.item(i).setForeground(Qt.red)

    def accept(self):
        self.selectedMaterial()
        QDialog.accept(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MaterialLibrary()
    win.show()
    app.exec_()
