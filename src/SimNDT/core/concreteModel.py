from PySide.QtGui import *
from PySide.QtCore import *

import time
import random
import numpy as np

from SimNDT.core.packing import Ellipse, Quadtree, ellipseMatrix, Rect, ellipseDiscard, circleMatrix


class Granulometry:
    def __init__(self, MI, NI, Pixel_mm, Dmin, Dmax, nG, AspectMin, AspectMax, Fraction, Label):
        self.AspectMax = AspectMax
        self.AspectMin = AspectMin
        self.Label = Label

        d = np.logspace(np.log10(Dmin), np.log10(Dmax), 12, endpoint=True).astype('float')
        A = np.zeros_like(d)
        A = 1. / (1.0 - ((Dmin) / Dmax) ** nG)
        A *= ((d / Dmax) ** nG - (Dmin / Dmax) ** nG)

        a = np.around((d[0:] / 2.) * 1000. * Pixel_mm)
        c = np.zeros((np.size(a),), dtype=np.float32)
        c = (A[1:] - A[:-1]) * Fraction / 100.
        self.a_reversed = a[::-1]
        self.c_reversed = c[::-1] * MI * NI

    def getB(self, a):
        return ((self.AspectMin) + (self.AspectMax - self.AspectMin) * random.random()) * a


class TwoPhaseModel:
    def __init__(self, MI, NI, granulometry, matrixLabel):

        self.MI = MI
        self.NI = NI
        self.granulometry = granulometry
        self.matrixLabel = matrixLabel

        xv = np.linspace(0, self.MI - 1, self.MI, endpoint=True).astype(np.int32)
        yv = np.linspace(0, self.NI - 1, self.NI, endpoint=True).astype(np.int32)
        X, Y = np.meshgrid(xv, yv)

        self.coords = {(x, y) for x, y in zip(X.ravel(), Y.ravel())}

        depth = 5
        self.qtree = Quadtree(depth, Rect(0, 0, self.MI, self.NI))
        (self.XX, self.YY) = np.meshgrid(range(0, self.NI), range(0, self.MI))

    def compute(self, progressBar):

        Objs = []
        Image = np.ones((self.MI, self.NI), np.float32) * self.matrixLabel
        # mask = np.zeros((self.MI,self.NI), np.float32)


        start = time.time()

        progressBar.setVisible(True)
        progressBar.setValue(0)
        QApplication.processEvents()

        total = len(self.granulometry.a_reversed)

        for ix, value in enumerate(zip(self.granulometry.a_reversed, self.granulometry.c_reversed)):
            print(ix, value[0], value[1])
            progressBar.setValue(100 * ix / float(total))
            QApplication.processEvents()

            area_set = 0
            while area_set < value[1]:

                cy, cx = self.coords.pop()
                if Image[cy, cx] == self.matrixLabel:

                    b = self.granulometry.getB(value[0])
                    theta = random.uniform(0, 2 * np.pi)

                    c = Ellipse(cy, cx, value[0], b, theta)
                    objs = self.qtree.query(c)
                    if len(objs) == 0:
                        self.qtree.insert(c)
                        Objs.append(c)
                        area_set += np.floor(c.area())
                        ellipseDiscard(c.y, c.x, c.a, c.b, c.theta, self.XX, self.YY, self.coords, Image,
                                       self.granulometry.Label)

                    else:
                        self.coords.add((cy, cx))

        print("draw")
        print(time.time() - start)

        """
        total = len(Objs)
        for idx, item in enumerate(Objs):
            if idx % 100 == 0:
                progressBar.setValue(100*idx/float(total))
                QApplication.processEvents()
            Image = ellipseMatrix(item.y, item.x, item.a, item.b, item.theta, Image, self.granulometry.Label, self.XX, self.YY)

        print time.time()-start
        """

        progressBar.setVisible(False)
        return Image

    def toDict(self):
        pass


class ThreePhaseModel:
    def __init__(self, MI, NI, granulometry, granulometry2, matrixLabel):

        self.MI = MI
        self.NI = NI
        self.granulometry = granulometry
        self.granulometry2 = granulometry2
        self.matrixLabel = matrixLabel

        xv = np.linspace(0, self.MI - 1, self.MI, endpoint=True).astype(np.int32)
        yv = np.linspace(0, self.NI - 1, self.NI, endpoint=True).astype(np.int32)
        X, Y = np.meshgrid(xv, yv)

        self.coords = {(x, y) for x, y in zip(X.ravel(), Y.ravel())}

        depth = 5
        self.qtree = Quadtree(depth, Rect(0, 0, self.MI, self.NI))
        (self.XX, self.YY) = np.meshgrid(range(0, self.NI), range(0, self.MI))

    def compute(self, progressBar):

        Objs1 = []
        Objs2 = []
        Image = np.ones((self.MI, self.NI), np.float32) * self.matrixLabel
        # mask = np.zeros((self.MI,self.NI), np.float32)

        start = time.time()

        progressBar.setVisible(True)
        progressBar.setValue(0)
        QApplication.processEvents()

        total = len(self.granulometry.a_reversed)

        for ix, value in enumerate(zip(self.granulometry.a_reversed, self.granulometry.c_reversed)):
            print(ix, value[0], value[1])
            progressBar.setValue(100 * ix / float(total))
            QApplication.processEvents()

            area_set = 0
            while area_set < value[1]:

                cy, cx = self.coords.pop()
                if Image[cy, cx] == self.matrixLabel:

                    b = self.granulometry.getB(value[0])
                    theta = random.uniform(0, 2 * np.pi)

                    c = Ellipse(cy, cx, value[0], b, theta)
                    objs = self.qtree.query(c)

                    if len(objs) == 0:
                        self.qtree.insert(c)
                        Objs1.append(c)
                        area_set += np.floor(c.area())
                        ellipseDiscard(c.y, c.x, c.a, c.b, c.theta, self.XX, self.YY, self.coords, Image,
                                       self.granulometry.Label)

                    else:
                        self.coords.add((cy, cx))

        print("draw")
        print(time.time() - start)

        """
        total = len(Objs1)
        for idx, item in enumerate(Objs1):
            if idx % 100 == 0:
                progressBar.setValue(100*idx/float(total))
                QApplication.processEvents()
            Image = ellipseMatrix(item.y, item.x, item.a, item.b, item.theta, Image, self.granulometry.Label, self.XX, self.YY)

        print time.time()-start
        """

        progressBar.setValue(0)
        QApplication.processEvents()

        total = len(self.granulometry2.a_reversed)

        for ix, value in enumerate(zip(self.granulometry2.a_reversed, self.granulometry2.c_reversed)):
            print(ix, value[0], value[1])
            progressBar.setValue(100 * ix / float(total))
            QApplication.processEvents()

            area_set = 0
            while area_set < value[1]:

                cy, cx = self.coords.pop()
                if Image[cy, cx] == self.matrixLabel:

                    c = Ellipse(cy, cx, value[0], value[0], 0)
                    objs = self.qtree.query(c)
                    if len(objs) == 0:
                        self.qtree.insert(c)
                        Objs2.append(c)
                        area_set += np.floor(c.area())
                        ellipseDiscard(c.y, c.x, c.a, c.b, c.theta, self.XX, self.YY, self.coords, Image,
                                       self.granulometry2.Label)

                    else:
                        self.coords.add((cy, cx))

        print("draw")
        print(time.time() - start)

        """
        total = len(Objs2)
        for idx, item in enumerate(Objs2):
            if idx % 20 == 0:
                progressBar.setValue(100*idx/float(total))
                QApplication.processEvents()
            Image = circleMatrix(item.y, item.x, item.a, Image, self.granulometry2.Label, self.XX, self.YY)

        print time.time()-start
        """

        progressBar.setVisible(False)
        return Image
