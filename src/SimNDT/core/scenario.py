__author__ = 'Miguel Molero'


import numpy as np
from scipy.misc  import imread, imrotate

from SimNDT.core.constants import *
from SimNDT.core.boundary import Boundary


class Scenario:

    def __init__(self, Width = 40, Height = 40, Pixel_mm =10, Label=0):

        self.Width		 = Width
        self.Height		 = Height
        self.Pixel_mm	 = Pixel_mm
        self.Label		 = Label

        self.M	 = int(self.Height * self.Pixel_mm)
        self.N	 = int(self.Width  * self.Pixel_mm)
        self.I	 = np.ones((self.M,self.N), dtype=np.uint8)*Label
        self.Iabs	 = 0
        self.Io      = np.ones((self.M,self.N), dtype=np.uint8)*Label
        self.Tap	 = list()

        self.BC      = False




    def setImage(self,I, Width, Height, Pixel_mm, Label):
        self.I = np.copy(I).astype(np.uint8)
        self.Io = np.copy(I).astype(np.uint8)
        self.Width = Width
        self.Height = Height
        self.Pixel_mm = Pixel_mm
        self.Label = Label
        self.M = int(self.Height * self.Pixel_mm)
        self.N = int(self.Width * self.Pixel_mm)

        self.resetBoundary()


    def resetBoundary(self):
        self.Iabs		 = 0
        self.Tap		 = list()
        self.BC          = False

    def __str__(self):
        return "Scenario: "

    def __repr__(self):
        return "Scenario: "


    def createBoundaries(self,boundaries):

        self.M, self.N	 = np.shape(self.I)
        self.Width = int(self.N/float(self.Pixel_mm))
        self.Height = int(self.N/float(self.Pixel_mm))
        self.resetBoundary()


        for boundary in boundaries:

            if boundary.BC == BC.AirLayer:
                size = 1
            else:
                size = boundary.Size * self.Pixel_mm

            if boundary.Name == "Top":
                topSize = size
            elif boundary.Name == "Bottom":
                bottomSize = size
            elif boundary.Name == "Left":
                leftSize = size
            elif boundary.Name == "Right":
                rightSize = size

        self.Tap = np.array([topSize, bottomSize, leftSize, rightSize])
        self.Iabs  = self.applyBoundaries(self.I)
        self.BC = True


    def applyBoundaries(self, I):

        self.Tap = np.int32(self.Tap)
        M_abs		 = int( self.M	 + self.Tap[0]	+ self.Tap[1] )
        N_abs		 = int( self.N	 + self.Tap[2]  + self.Tap[3] )

        Iabs		 = 255*np.ones((int(M_abs),int(N_abs)),dtype=np.uint8)
        Iabs[self.Tap[0] : M_abs-self.Tap[1], self.Tap[2] : N_abs-self.Tap[3]] = np.copy(I)
        return Iabs


    def updateScenario(self):
        if self.BC:
            self.Iabs = self.applyBoundaries(self.I)


    def addEllipse(self, x0, y0, a, b, theta, Label):

        x0 *= self.Pixel_mm
        y0 *= self.Pixel_mm
        a  *= self.Pixel_mm
        b  *= self.Pixel_mm

        (x,y)	= np.meshgrid(range(0,self.N),range(0,self.M))

        Ellipse = ( ( ( (x-x0)*np.cos(theta)+(y-y0)*np.sin(theta) )**2 )/(a**2) +
                    ( ( (x-x0)*np.sin(theta)-(y-y0)*np.cos(theta) )**2 )/(b**2) )

        Img	 = (Ellipse < 1.0)
        indx,indy = np.nonzero(Img == 1)
        self.I[indx,indy] = Label

        self.updateScenario()


    def resetImage(self):

        self.resetBoundary()
        self.I	= np.copy(self.Io)



    def addObject(self, obj):

        if obj.Name == "ellipse":

            a = obj.a
            b = obj.b
            theta = obj.theta
            Label = obj.Label
            x0 = obj.x0 * self.Pixel_mm
            y0 = obj.y0 * self.Pixel_mm
            self.addEllipse(x0, y0, a, b, theta, Label)


        elif obj.Name == "circle":

            x0 = obj.x0
            y0 = obj.y0
            a  = obj.r
            Label = obj.Label
            self.addEllipse(x0, y0, a, a, 0, Label)


        elif obj.Name == "square":

            x0 = obj.x0
            y0 = obj.y0
            L  = obj.L
            theta = obj.theta
            Label = obj.Label
            self.addRectangle(x0, y0, L, L, theta, Label)

        elif obj.Name == "rectangle":

            x0 = obj.x0
            y0 = obj.y0
            W  = obj.W
            H  = obj.H
            theta = obj.theta
            Label = obj.Label
            self.addRectangle(x0, y0, W, H, theta, Label)




    def addRectangle(self, W_0, H_0, W, H, Theta,Label):
        """
        Create a rectangle
        W_0, H_0:  center of rectangle
        W,H		:  dimension of rectangle
        """

        a = round(H*self.Pixel_mm/2.0)
        b = round(W*self.Pixel_mm/2.0)
        angle = Theta * np.pi/180.0
        H0 = H_0*self.Pixel_mm
        W0 = W_0*self.Pixel_mm

        if angle == 0:
            size_a = 4*a
            size_b = 4*b

            vectX = np.int32(np.linspace(-a,a, size_a) + H0)
            vectY = np.int32(np.linspace(-b,b, size_b) + W0)
            for	x in vectX:
                for y in vectY:
                    self.I[x, y] = Label

        else:
            size_a = 4*a
            size_b = 4*b

            for	 x in  np.linspace(-a,a,size_a):
                for y in np.linspace(-b,b,size_b):
                    _xr = np.int32(np.cos(angle)*x - np.sin(angle)*y + H0)
                    _yr = np.int32(np.sin(angle)*x + np.cos(angle)*y + W0)
                    self.I[_xr,_yr] = Label

        self.updateScenario()


    def rotate(self, angle=90, direction="clockwise"):
        if direction == "clockwise":
            self.I = imrotate(self.I,-1*angle, interp = 'nearest')
            self.M, self.N = np.shape(self.I)

            if np.size(self.Iabs) > 1:
                self.Iabs = imrotate(self.Iabs,-1*angle, interp = 'nearest')

        else:
            self.I = imrotate(self.I,angle, interp = 'nearest')
            self.M, self.N = np.shape(self.I)

            if np.size(self.Iabs) > 1:
                self.Iabs = imrotate(self.Iabs,angle, interp = 'nearest')








