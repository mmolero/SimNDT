__author__ = 'Miguel'




import os, sys
from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.graphics.mplWidget import MplCanvas
from SimNDT.gui.ui_loadimagemainwindow import Ui_LoadImageMainWindow
from SimNDT.gui.Warnings import WarningParms
from SimNDT.gui.constants import *

import numpy as np
from scipy.misc  import imread, imrotate
from scipy.ndimage.filters import median_filter



from scipy.cluster.vq import kmeans2, kmeans
import  matplotlib.cm as cm


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])



class LoadImageWindowMain(QMainWindow, Ui_LoadImageMainWindow):

	def __init__(self, parent=None):
		super(LoadImageWindowMain, self).__init__(parent)
		self.setupUi(self)

		self.colormapComboBox = QComboBox()
		self.colormapComboBox.addItems(['jet','spectral','other'])
		self.colormapComboBox.setEnabled(False)

		self.infoLabel = QLabel("Info")
		self.statusLabel = QLabel("Status")
		self.moreInfoLabel = QLabel("More Info")
		self.toolBar.addWidget(self.colormapComboBox)
		self.toolBar.addSeparator()
		self.toolBar.addWidget(self.infoLabel)
		self.toolBar.addSeparator()
		self.toolBar.addWidget(self.statusLabel)
		self.toolBar.addSeparator()
		self.toolBar.addWidget(self.moreInfoLabel)


	def setEnabledToolbar(self, state):

		self.actionFlip_Horizontal.setEnabled(state)
		self.actionFlip_Vertical.setEnabled(state)
		self.actionRotate_90_Clockwise.setEnabled(state)
		self.actionRotate_90_Counter_Clockwise.setEnabled(state)
		self.actionShow_Original_Image.setEnabled(state)


		self.numberLabelsLabel.setVisible(state)
		self.PixelLabel.setVisible(state)


		self.getLabeledImagePushButton.setVisible(state)
		self.numberLabelsSpinBox.setVisible(state)
		self.PixelLineEdit.setVisible(state)



class LoadScenarioFromImage(QDialog):


	def __init__(self, filename= None, parent=None):
		super(LoadScenarioFromImage, self).__init__(parent)
		self.init()
		self.connectionSetup()

		self.filename = filename
		self.imageToDraw = None
		self.Pixel = None




	def init(self):



		self.mainwindow = LoadImageWindowMain()
		self.mainwindow.setEnabledToolbar(False)

		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
		self.connect(buttonBox, SIGNAL("rejected()"), self, SLOT("reject()"))

		layout = QVBoxLayout()
		layout.addWidget(self.mainwindow)
		layout.addWidget(buttonBox)
		self.setLayout(layout)

		w =  self.mainwindow.imageFrame.width()
		h =  self.mainwindow.imageFrame.height()

		self.mpl = MplCanvas(width=int(w/100.0), height=int(h/100.0), dpi=100)
		self.mpl.ax.axis("off")

		imageLayout = QVBoxLayout()
		imageLayout.addWidget(self.mpl)

		self.mainwindow.imageFrame.setLayout(imageLayout)
		self.mainwindow.infoLabel.clear()
		self.mainwindow.statusLabel.clear()
		self.mainwindow.moreInfoLabel.clear()




	def connectionSetup(self):
		self.mainwindow.actionOpen_Image.triggered.connect(self.openImage)
		self.mainwindow.actionShow_Original_Image.triggered.connect(self.showOriginalImage)
		self.mainwindow.actionRotate_90_Clockwise.triggered.connect(self.rotate90ClockWise)
		self.mainwindow.actionRotate_90_Counter_Clockwise.triggered.connect(self.rotate90CounterClockWise)
		self.mainwindow.actionFlip_Horizontal.triggered.connect(self.flipHorizontal)
		self.mainwindow.actionFlip_Vertical.triggered.connect(self.flipVertical)
		self.mainwindow.colormapComboBox.currentIndexChanged.connect(self.changeColormap)
		self.mainwindow.getLabeledImagePushButton.pressed.connect(self.getLabeledImage)




	def openImage(self):



		self.mainwindow.statusLabel.clear()
		self.mainwindow.moreInfoLabel.clear()


		self.labels = None
		self.image_labeled = None

		dir = os.path.dirname(self.filename) if self.filename is not None else "."
		fname, filters =  QFileDialog.getOpenFileName(None, "Load Image", dir,  self.tr("Image Files (*.png *.jpg *.bmp *.jpeg)"))

		if fname:

			self.imageOriginal   = imread(fname)
			try:
				M,N, R = np.shape(self.imageOriginal)
				self.mainwindow.colormapComboBox.setEnabled(False)
			except:
				M,N = np.shape(self.imageOriginal)
				self.mainwindow.colormapComboBox.setEnabled(True)




			self.imageToDraw = self.imageOriginal
			self.mainwindow.setEnabledToolbar(True)
			self.updateImage()



	def changeColormap(self, index):

		if self.imageToDraw is not None:

			if index==0:
				Colormap = cm.jet
			elif index ==1:
				Colormap = cm.spectral
			elif index ==2:
				Colormap = cm.Set1

			self.mpl.fig.clear()
			self.mpl.ax  = self.mpl.fig.add_subplot(111)
			cax  = self.mpl.ax.imshow(self.imageToDraw, cmap = Colormap, vmin=0, vmax = 255)
			self.showColorbar(cax)
			self.mpl.ax.axis("off")
			self.mpl.draw()
			QCoreApplication.processEvents()



			return cax




	def showOriginalImage(self):

		self.mainwindow.statusLabel.clear()
		self.mainwindow.moreInfoLabel.clear()

		self.imageToDraw = self.imageOriginal
		self.updateImage()


	def rotate90ClockWise(self):

		self.imageToDraw = imrotate(self.imageToDraw,-90, interp = 'nearest')
		self.updateImage()

	def rotate90CounterClockWise(self):

		self.imageToDraw = imrotate(self.imageToDraw,90, interp = 'nearest')
		self.updateImage()


	def flipHorizontal(self):

		self.imageToDraw = np.fliplr(self.imageToDraw)
		self.updateImage()



	def flipVertical(self):

		self.imageToDraw = np.flipud(self.imageToDraw)
		self.updateImage()

	def updateImage(self):

		self.mainwindow.statusLabel.clear()
		self.mainwindow.moreInfoLabel.clear()

		self.mpl.ax.imshow(self.imageToDraw)
		self.mpl.ax.axis("off")
		self.mpl.draw()
		QCoreApplication.processEvents()

		try:
			M,N, R = np.shape(self.imageToDraw)
			self.mainwindow.colormapComboBox.setEnabled(False)
		except:
			M,N = np.shape(self.imageToDraw)

		self.mainwindow.infoLabel.setText("Dimensions: %d x %d"%(M,N))


	def getLabeledImage(self):

		self.labels = None

		self.mainwindow.colormapComboBox.setEnabled(True)
		self.mainwindow.statusLabel.setText(self.tr("Procesing......"))
		QCoreApplication.processEvents()

		try:
			M,N, R = np.shape(self.imageToDraw)
			self.image_gray = rgb2gray(self.imageToDraw)
		except:
			M,N = np.shape(self.imageToDraw)


		n_colors = self.mainwindow.numberLabelsSpinBox.value()
		self.image = median_filter(self.image_gray,2)
		image_array = np.reshape(self.image, (M*N,1))
		centroids, self.labels = kmeans2(image_array, n_colors)
		check =  np.size(np.unique(self.labels))

		if check != n_colors:
			self.image_labeled = np.zeros((M,N))
			self.mpl.fig.clear()
			self.mpl.ax  = self.mpl.fig.add_subplot(111)
			self.mpl.ax.imshow(np.zeros((M,N)), cmap = cm.jet, vmin=0, vmax = 255)
			self.mpl.ax.axis("off")
			self.mpl.draw()

			QCoreApplication.processEvents()
			msgBox = WarningParms("Try again")
			if msgBox.exec_():
				self.mainwindow.statusLabel.clear()
				QCoreApplication.processEvents()
				return


		self.labels *= 40


		self.image_labeled = np.reshape(self.labels, (M,N))
		self.imageToDraw = self.image_labeled

		index = self.mainwindow.colormapComboBox.currentIndex()
		cax = self.changeColormap(index)

		self.mpl.draw()
		self.mainwindow.moreInfoLabel.setText(self.tr("<b>Apply several times to change labels"))
		self.mainwindow.statusLabel.setText(self.tr("Done"))
		QCoreApplication.processEvents()


	def showColorbar(self, cax):

		if self.labels is not None:

			ticks_at = np.unique(self.labels)
			cbar = self.mpl.fig.colorbar(cax, ticks=ticks_at, orientation='horizontal')
			cbar.set_label("Labels")


	def accept(self):


		if self.image_labeled is None:
			msgBox = WarningParms("Get the labeled Image")
			if msgBox.exec_():
				return

		try:
			self.Pixel = float(self.mainwindow.PixelLineEdit.text())

		except:
			msgBox = WarningParms("Please give correctly the Pixel/mm")
			if msgBox.exec_():
				return

		QDialog.accept(self)





