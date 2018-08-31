__author__ = 'Miguel  Molero'



import copy, os

from PySide.QtCore import *
from PySide.QtGui import *


try:
    import cv2
except:
    print ("problem at importing cv2")


from SimNDT.gui.HelperMethods import sort_nicely
from SimNDT.gui.ui_generatevideo import Ui_generateVideoDialog

from SimNDT.gui.Warnings import WarningParms, DoneParms


class GenerateVideo(QDialog, Ui_generateVideoDialog):

    def __init__(self, parent = None):
        super(GenerateVideo, self).__init__(parent)
        self.setupUi(self)

        self.addImagesPushButton.pressed.connect(self.addImages)
        self.videoBasenamePushButton.pressed.connect(self.videoBasename)

        self.dirpath = None
        self.FilenameVideo = None
        self.Images = None



    def addImages(self):

        fnames = "."
        fnames, filters =  QFileDialog.getOpenFileNames(None, "Choose the image files", fnames,  self.tr("Image Files (*.png *.jpg *.bmp *.jpeg)"))

        if fnames is not None:
            sort_nicely(fnames)
            self.listWidget.addItems(fnames)
            self.Images =  fnames



    def videoBasename(self):

        dir = os.path.dirname(self.dirpath) if self.dirpath is not None else "."
        formats = ["*.%s" % unicode("avi")]
        fname = None
        fname, filters = QFileDialog.getSaveFileName(None, "New Simulation File (.avi)", dir,"avi Files (%s)"%" ".join(formats))

        if fname is not None:
            self.FilenameVideo = fname
            self.videoBasenameLineEdit.setText(self.FilenameVideo)


    def accept(self):


        if self.Images is None:
            msgBox = WarningParms("Please add Images to generate the video")
            if msgBox.exec_():
                return

        if self.FilenameVideo is None:
            msgBox = WarningParms("Please define the video name")
            if msgBox.exec_():
                return

        if len(self.Images) < 10:
            msgBox = WarningParms("Please add more Images")
            if msgBox.exec_():
                return


        FPS = self.fPSSpinBox.value()

        print("start")
        img = cv2.imread(self.Images[0])
        height , width , layers =  img.shape
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        video = cv2.VideoWriter(self.FilenameVideo, fourcc=fourcc,
                                    fps=FPS, frameSize=(width,height))


        try:
            for item in self.Images:
                print(item)
                img = cv2.imread(item)
                video.write(img)

            cv2.destroyAllWindows()
            video.release()
            print("end")

        except:
            msgBox = WarningParms("Impossible to generate the video using the given images!!!!")
            if msgBox.exec_():
                return


        QDialog.accept(self)