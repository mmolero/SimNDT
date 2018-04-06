__author__ = 'Miguel Molero'

import time
import numpy as np
from concreteModel import Granulometry, ellipseDiscard
from quadtree import Quadtree, Rect, Ellipse, ellipseMatrix
import random


class TwoPhaseModel:

    def __init__(self, MI, NI, granulometry, matrixLabel):

        self.MI = MI
        self.NI = NI
        self.granulometry = granulometry
        self.matrixLabel = matrixLabel

        xv = np.linspace(0, self.MI-1, self.MI, endpoint=True).astype(np.int32)
        yv = np.linspace(0, self.NI-1, self.NI, endpoint= True).astype(np.int32)
        X, Y = np.int32(np.meshgrid(xv,yv))

        self.coords = { (x,y) for x, y in zip(X.ravel(),Y.ravel()) }

        depth = 4
        self.qtree = Quadtree(int(depth), Rect(0, 0, int(self.MI), int(self.NI)))
        (self.XX,self.YY)= np.meshgrid(range(0,self.NI),range(0,self.MI))



    def compute(self):

        Objs = []
        Image = np.ones((self.MI,self.NI), np.int32) * self.matrixLabel
        Image = Image.astype(np.int32)


        start = time.time()

        for ix, value in enumerate ( zip(self.granulometry.a_reversed, self.granulometry.c_reversed) ):
            print (ix, value[0], value[1])
            area_set = 0
            while area_set < value[1]:

                cy, cx = self.coords.pop()
                #if Image[cy,cx] == self.matrixLabel:
                if True:

                    b = self.granulometry.getB(value[0])
                    theta = random.uniform(0, np.pi)

                    c = Ellipse(cy, cx, int(value[0]), int(b), theta)
                    objs = self.qtree.query(c)
                    if len(objs)==0:
                        self.qtree.insert(c)
                        Objs.append(c)
                        area_set += c.area()

                        #ellipseMatrix(c.y(), c.x(), c.a(), c.b(), c.theta(), Image, int(self.granulometry.Label), self.XX, self.YY)
                        #ellipseDiscard(c.y(), c.x(), c.a(), c.b(), c.theta(), self.XX, self.YY, self.coords, Image, self.granulometry.Label)

                    else:
                        self.coords.add((cy,cx))


        print (time.time()-start)



        return Objs, int(self.granulometry.Label), self.XX, self.YY, Image

if __name__=='__main__':

    #import matplotlib.pyplot as plt

    MI, NI = 2000,2000
    granu = Granulometry(MI=MI, NI=NI, Pixel_mm=10, Dmin=0.5e-3, Dmax=10e-3, nG=0.01, AspectMin=0.5, AspectMax=0.9, Fraction=50, Label=40)
    model = TwoPhaseModel(MI,NI, granu, 0)
    Objs, Label, XX, YY, Image = model.compute()

    """
    print "draw"
    for c in Objs:
        ellipseMatrix(c.y(), c.x(), c.a(), c.b(), c.theta(), Image, Label, XX, YY)
    """

    #plt.figure()
    #plt.imshow(I)
    #plt.show()