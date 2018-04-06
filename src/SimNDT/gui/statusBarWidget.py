__author__ = 'Miguel Molero'

from PySide.QtCore import *
from PySide.QtGui import *


class StatusBarWidget(QWidget):
    def __init__(self, parent=None):
        super(StatusBarWidget, self).__init__(parent)

        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 1000)
        self.zoomSpinBox.setSuffix("%")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip(self.tr("Zoom the scenario"))
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        # self.zoom_SpinBox.setFocusPolicy(Qt.NoFocus)
        self.zoomSpinBox.setVisible(False)

        self.statusFrame = QFrame()
        self.statusFrame.setFrameStyle(QFrame.Sunken)
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        self.barStatus = QProgressBar()
        self.barStatus.setVisible(False)
        self.barStatus.setMinimumWidth(80)
        self.barStatus.setMaximumWidth(100)
        self.barStatus.setRange(0, 100)
        self.barStatus.setValue(0)
        self.barStatus.setTextVisible(True)

        self.labelStatusBar = QLabel()
        label_space = QLabel(" ")
        self.labelStatusBar.hide()

        self.labelInspectionStatusBar = QLabel()
        self.labelInspectionStatusBar.hide()

        self.StartPauseStatusBar = QPushButton(QIcon(":/pause.png"), "")
        self.StopStatusBar = QPushButton(QIcon(":/stop.png"), "")
        self.StartPauseStatusBar.hide()
        self.StopStatusBar.hide()

        self.openclFrame = QFrame()
        openclLayout = QHBoxLayout()
        self.openclIcon = QLabel()
        self.openclIcon.setPixmap(QPixmap(":/opencl.png").scaled(30, 30))
        self.openclIcon.setToolTip(self.tr("OpenCL is not actived"))

        self.openclLabel = QLabel()
        self.openclLabel.setPixmap(QPixmap(":/circle_red.png").scaled(10, 10))
        openclLayout.addWidget(self.openclIcon)
        openclLayout.addWidget(self.openclLabel)
        self.openclFrame.setLayout(openclLayout)

        layout.addWidget(self.StartPauseStatusBar)
        layout.addWidget(self.StopStatusBar)
        layout.addWidget(self.labelInspectionStatusBar)
        layout.addWidget(self.labelStatusBar)
        layout.addWidget(self.barStatus)
        layout.addWidget(self.zoomSpinBox)
        layout.addWidget(self.openclFrame)

        layout.addWidget(label_space)

        self.statusFrame.setLayout(layout)
        self.statusFrame.layout().setSizeConstraint(QLayout.SetFixedSize)

    def startSimulation(self, TimeSteps):
        self.barStatus.show()
        self.StopStatusBar.show()
        self.labelStatusBar.setText("%d - %d" % (0, TimeSteps))
        self.labelStatusBar.show()
        QCoreApplication.processEvents()

    def endSimulation(self):
        self.barStatus.setValue(0)
        self.barStatus.hide()
        self.StopStatusBar.hide()
        self.StartPauseStatusBar.hide()
        self.labelStatusBar.setText("")
        self.labelStatusBar.hide()
        self.labelInspectionStatusBar.setText("")
        self.labelInspectionStatusBar.hide()
        QCoreApplication.processEvents()

    def viewOn(self):
        self.StartPauseStatusBar.show()
        self.updateGeometryFrame()

    def updateGeometryFrame(self):
        self.statusFrame.updateGeometry()
        QCoreApplication.processEvents()
