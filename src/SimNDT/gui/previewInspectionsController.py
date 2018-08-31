__author__ = 'Miguel Molero'

import time

from PySide.QtGui import *
from PySide.QtCore import *
from SimNDT.graphics.mplWidget import MplCanvas

import numpy as np


class PreviewSingleLaunch(QDialog):
    def __init__(self, method, scenario, transducer, parent=None):
        super(PreviewSingleLaunch, self).__init__(parent)
        self.parent = parent

        mpl = MplCanvas(self, width=3, height=3, dpi=100)

        M, N = np.shape(scenario.I)
        Pixel_mm = scenario.Pixel_mm

        XL, YL = method.view(M, N, Pixel_mm, method.Theta, transducer)

        mpl.ax.imshow(scenario.I, vmin=0, vmax=255)
        mpl.ax.hold(True)
        mpl.ax.plot(YL, XL, 'ks')
        mpl.ax.axis('off')

        w = QWidget(self)
        h = QVBoxLayout()
        h.addWidget(mpl)
        w.setLayout(h)

        layout = QVBoxLayout()
        layout.addWidget(w)

        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr("Preview"))
        self.setWindowIcon(QIcon(":/previewImage.png"))


class PreviewLinearScan(QDialog):
    def __init__(self, method, inspection, scenario, transducer, parent=None):
        super(PreviewLinearScan, self).__init__(parent)
        self.parent = parent

        self.mpl = MplCanvas(width=5, height=5, dpi=100)
        self.mpl.ax.axis('off')

        layout = QVBoxLayout()
        layout.addWidget(self.mpl)

        self.setLayout(layout)

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr("Preview"))
        self.setWindowIcon(QIcon(":/previewImage.png"))

        self.method = method
        self.inspection = inspection
        self.scenario = scenario
        self.transducer = transducer
        QTimer.singleShot(300, self.Show)

    def Show(self):
        M, N = np.shape(self.scenario.I)
        Pixel_mm = self.scenario.Pixel_mm

        for offset in self.inspection.ScanVector:
            self.transducer.CenterOffset = offset
            XL, YL = self.method.view(M, N, Pixel_mm, self.method.Theta, self.transducer)
            self.mpl.ax.imshow(self.scenario.I, vmin=0, vmax=255)
            self.mpl.ax.hold(True)
            self.mpl.ax.plot(YL, XL, 'ks')
            self.mpl.ax.axis('off')
            self.mpl.ax.hold(False)
            self.mpl.draw()
            QCoreApplication.processEvents()
            time.sleep(0.25)


class PreviewTomography(QDialog):
    def __init__(self, inspection, scenario, transducer, parent=None):
        super(PreviewTomography, self).__init__(parent)
        self.parent = parent

        self.mpl = MplCanvas(width=5, height=5, dpi=100)
        self.mpl.ax.axis('off')

        layout = QVBoxLayout()
        layout.addWidget(self.mpl)

        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.tr("Preview"))
        self.setWindowIcon(QIcon(":/previewImage.png"))

        self.inspection = inspection
        self.scenario = scenario
        self.transducer = transducer
        QTimer.singleShot(300, self.Show)

    def Show(self):
        M, N = np.shape(self.scenario.I)
        Pixel_mm = self.scenario.Pixel_mm
        DiameterRing = self.inspection.DiameterRing
        Theta = self.inspection.Theta

        XL, YL = self.inspection.view(M, N, DiameterRing, Pixel_mm, Theta, self.transducer)
        self.mpl.ax.imshow(self.scenario.I, vmin=0, vmax=255)
        self.mpl.ax.hold(True)
        self.mpl.ax.plot(YL, XL, 'ks')
        self.mpl.ax.axis('off')
        self.mpl.ax.hold(False)
        self.mpl.draw()
