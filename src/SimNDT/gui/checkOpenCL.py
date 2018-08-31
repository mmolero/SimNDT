__author__ = 'Miguel Molero'

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

global ErrorImportCL
try:
    import pyopencl    as    cl

    ErrorImportCL = False
except ImportError:
    ErrorImportCL = True


def isOpenCL(openclIcon, openclLabel):
    global ErrorImportCL
    if not ErrorImportCL:
        openclIcon.setToolTip(("OpenCL actived"))
        openclLabel.setPixmap(QPixmap(":/circle_green.png").scaled(10, 10))
