__author__ = 'Miguel Molero'
from SimNDT.graphics.mplWidget import *
from matplotlib import cm


class PreviewScenario(QDialog):
    def __init__(self, Scenario, parent=None):
        super(PreviewScenario, self).__init__(parent)
        self.parent = parent

        self.mpl = MplCanvas(width=6, height=6, dpi=100)
        self.mpl.ax.axis("off")
        self.mpl_toolbar = NavigationToolbar(self.mpl, self)

        self.colormapComboBox = QComboBox()
        self.colormapComboBox.addItems(['jet', 'spectral', 'other'])
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Colormap"))
        hbox.addWidget(self.colormapComboBox)
        hbox.addStretch()

        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        frame.setLayout(hbox)
        frame.setMaximumHeight(50)

        layout = QVBoxLayout()
        layout.addWidget(self.mpl)
        layout.addWidget(frame)
        layout.addWidget(self.mpl_toolbar, 0)
        self.setLayout(layout)

        self.colormapComboBox.currentIndexChanged.connect(self.change)

        # self.layout().setSizeConstraint(QLayout.SetFixedSize)
        # On Top
        self.setWindowFlags(self.windowFlags())
        self.setWindowTitle(self.tr("Preview the Labeled Scenario"))
        self.setWindowIcon(QIcon(":/previewImage.png"))

        self.Scenario = Scenario

        cax = self.mpl.ax.imshow(self.Scenario.I, cmap=cm.jet, vmin=0, vmax=255)
        ticks_at = np.unique(self.Scenario.I)
        cbar = self.mpl.fig.colorbar(cax, ticks=ticks_at, orientation='horizontal')
        cbar.set_label("Labels")
        self.mpl.draw()
        QApplication.processEvents()

    def change(self, index):

        if index == 0:
            Colormap = cm.jet
        elif index == 1:
            Colormap = cm.spectral
        elif index == 2:
            Colormap = cm.Set1

        self.mpl.fig.clear()
        self.mpl.ax = self.mpl.fig.add_subplot(111)

        cax = self.mpl.ax.imshow(self.Scenario.I, cmap=Colormap, vmin=0, vmax=255)
        ticks_at = np.unique(self.Scenario.I)
        cbar = self.mpl.fig.colorbar(cax, ticks=ticks_at, orientation='horizontal')
        cbar.set_label("Labels")

        self.mpl.draw()
        QApplication.processEvents()
