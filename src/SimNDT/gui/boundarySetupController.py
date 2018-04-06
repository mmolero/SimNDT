__author__ = 'Miguel'


from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.ui_boundarysetup import Ui_boundarySetupDialog
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.constants import *

from SimNDT.core.constants import *
from SimNDT.core.boundary import Boundary
import copy


class BoundarySetup(QDialog,Ui_boundarySetupDialog):

	def __init__(self, SimNDT_Boundaries, parent = None):
		super(BoundarySetup,self).__init__(parent)
		self.setupUi(self)
		self.connectionSetup()

		if SimNDT_Boundaries is not None:
			for boundary in SimNDT_Boundaries:
				self.setupBC(boundary)
		else:
			self.topComboBox.setCurrentIndex(BC.AirLayer)
			self.bottomComboBox.setCurrentIndex(BC.AirLayer)
			self.leftComboBox.setCurrentIndex(BC.AirLayer)
			self.rightComboBox.setCurrentIndex(BC.AirLayer)


	def connectionSetup(self):
		self.connect(self.topComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.topComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.bottomComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.bottomComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.leftComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.leftComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.rightComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)
		self.connect(self.rightComboBox, SIGNAL("currentIndexChanged(int)"), self.setVisibleFunc)


	def setVisibleFunc(self, value):

		sender = self.sender()
		if  sender.objectName() == "topComboBox":
			self.topLayerSizeLabel.setVisible(not value)
			self.topLayerSizeLineEdit.setVisible(not value)
		elif sender.objectName() == "bottomComboBox":
			self.bottomLayerSizeLabel.setVisible(not value)
			self.bottomLayerSizeLineEdit.setVisible(not value)
		elif sender.objectName() == "leftComboBox":
			self.leftLayerSizeLabel.setVisible(not value)
			self.leftLayerSizeLineEdit.setVisible(not value)
		elif sender.objectName() == "rightComboBox":
			self.rightLayerSizeLabel.setVisible(not value)
			self.rightLayerSizeLineEdit.setVisible(not value)


	def setupBC(self, boundary):

		if boundary.Name == "Top":
			self.topComboBox.setCurrentIndex(boundary.BC)
			if boundary.BC == BC.AbsorbingLayer:
				self.topLayerSizeLabel.setVisible(True)
				self.topLayerSizeLineEdit.setVisible(True)
				self.topLayerSizeLineEdit.setText(unicode(boundary.Size))

		elif boundary.Name == "Bottom":
			self.bottomComboBox.setCurrentIndex(boundary.BC)
			if boundary.BC == BC.AbsorbingLayer:
				self.bottomLayerSizeLabel.setVisible(True)
				self.bottomLayerSizeLineEdit.setVisible(True)
				self.bottomLayerSizeLineEdit.setText(unicode(boundary.Size))

		elif boundary.Name == "Left":
			self.leftComboBox.setCurrentIndex(boundary.BC)
			if boundary.BC == BC.AbsorbingLayer:
				self.leftLayerSizeLabel.setVisible(True)
				self.leftLayerSizeLineEdit.setVisible(True)
				self.leftLayerSizeLineEdit.setText(unicode(boundary.Size))


		elif boundary.Name == "Right":
			self.rightComboBox.setCurrentIndex(boundary.BC)
			if boundary.BC == BC.AbsorbingLayer:
				self.rightLayerSizeLabel.setVisible(True)
				self.rightLayerSizeLineEdit.setVisible(True)
				self.rightLayerSizeLineEdit.setText(unicode(boundary.Size))




	def accept(self):

		try:
			items = [ (self.topComboBox,self.topLayerSizeLineEdit, "Top" ),
			          (self.bottomComboBox,self.bottomLayerSizeLineEdit,"Bottom" ),
			          (self.leftComboBox,self.leftLayerSizeLineEdit,"Left" ),
			          (self.rightComboBox,self.rightLayerSizeLineEdit,"Right" )]

			self.Boundaries = list()


			for item in items:
				index = item[0].currentIndex()
				if index == BC.AirLayer:
					Size = 0.0
				else:
					Size = float(item[1].text())
					if Size == 0:
						msgBox = WarningParms("Undefined Size (%s)!!!!" % item[2])
						if msgBox.exec_():
							return

				self.Boundaries.append(Boundary(item[2],index,Size))


		except:
			msgBox = WarningParms()
			if msgBox.exec_():
				return


		QDialog.accept(self)
