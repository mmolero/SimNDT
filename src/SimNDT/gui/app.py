import sys
import gc

from PySide.QtCore import *
from PySide.QtGui import *

from SimNDT.gui.resources_rc import *
from SimNDT.gui.MainWindow import Info

try:
    import Tkinter
    import FileDialog
except:
    pass

info = Info()

class SplashScreen(QSplashScreen):
    def __init__(self,  pixmap, f):
        super(SplashScreen, self).__init__(pixmap, f)
        self.m_progress= 0
        self.setCursor(Qt.BusyCursor)
        self.showMessage("SimNDT v{0}".format(info.version), Qt.AlignBottom | Qt.AlignRight, Qt.white)

    def drawContents(self, painter):
        QSplashScreen.drawContents(self, painter)

    def setProgress(self, value):

        self.m_progress = value
        if (self.m_progress > 100):
            self.m_progress = 100
        if (self.m_progress < 0):
            self.m_progress = 0
        self.update()


def run():
    app = QApplication(sys.argv)
    app.setOrganizationName("SimNDT")
    app.setOrganizationDomain("SimNDT.es")
    app.setApplicationName("SimNDT")
    app.setWindowIcon(QIcon(":/logo-SimNDT.bmp"))

    splash_pix = QPixmap(":/logo-SimNDT.bmp")
    splash = SplashScreen(splash_pix,  Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()


    import SimNDT.gui.MainWindow as mw
    app.processEvents()

    win = mw.MainWindow()
    win.show()
    splash.finish(win)
    app.exec_()

    win.deleteLater()
    app.flush()
    del win

    gc.collect()
    del app


