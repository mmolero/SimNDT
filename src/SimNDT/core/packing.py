import math
from math import pi

import numpy as np



class Ellipse:

    def __init__(self, x, y, a, b, theta):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.theta = theta
        self.rect = self.getRect()

    def area(self):
        return pi * self.a * self.b

    def getRect(self):

        t	= np.linspace(0,2*pi,20, endpoint=True)
        x	= self.x  + self.a * np.cos(t)
        y	= self.y  + self.b * np.sin(t)

        xmin = np.min(x)
        xmax = np.max(x)
        ymin = np.min(y)
        ymax = np.max(y)

        w = xmax-xmin
        h = ymax-ymin

        x0 = (xmax+xmin)/2
        y0 = (ymax+ymin)/2

        return Rect(x0,y0,w,h)



    def intersect2(self, b):
        return ( (np.abs(self.rect.x - b.rect.x) * 2.0 < (self.rect.w + b.rect.w) ) and
               (np.abs(self.rect.y - b.rect.y) * 2.0 < (self.rect.h + b.rect.h)) )



    def intersect(self, ellipse):

        c =	 np.sqrt(self.a**2 - self.b**2)
        cost  =	 c * np.cos(self.theta)
        sint  =	 c * np.sin(self.theta)
        d1	= (ellipse.x - self.x - cost)**2 + (ellipse.y - self.y - sint)**2
        d1	= np.sqrt(d1)
        d2	= (ellipse.x - self.x + cost)**2 + (ellipse.y - self.y + sint)**2
        d2	= np.sqrt(d2)
        d	= np.sqrt( (self.x-ellipse.x)**2 + (self.y-ellipse.y)**2 )

        if self.a >= 8*ellipse.a:
            Mb	= 0.15*self.a + ellipse.a

        elif ellipse.a >= 8*self.a:
            Mb	= self.a + 0.15*ellipse.a


        else:
            Mb	= self.a + ellipse.a

        if	(d1+d2 <= Mb) or (d <= Mb):
            return True

        return False





class Circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __str__(self):
        return '<{0},{1}:{2}>'.format(self.x, self.y, self.r)


    def area(self):
        return pi * self.r**2


    def distance(self, x, y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)


    def collide(self, x, y):
        return (self.distance(x, y) <= self.r)


    def intersect(self, circ):
        if (self.distance(circ.x, circ.y) <= self.r + circ.r):
            return True
        else:
            return False

    def getRect(self):

        return Rect(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)





class Rect:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


    def collide(self, x, y):
        return ((self.x <= x <= self.x + self.w) and
                 (self.y <= y <= self.y + self.h))

    def intersect(self, rect):
        return ((self.x < rect.x + rect.w) and (rect.x < self.x + self.w) and
                (self.y < rect.y + rect.h) and (rect.y < self.y + self.h))

    def __str__(self):
        return '<{0},{1};{2},{3}>'.format(self.x, self.y, self.w, self.h)



class Quadtree:

    def __init__(self, depth, rect):
        self.rect  = rect
        self.depth = depth
        self.ne = None
        self.se = None
        self.sw = None
        self.nw = None
        self.objs = list()
        if (depth > 1):
            w = self.rect.w / 2
            h = self.rect.h / 2
            x = self.rect.x + w
            y = self.rect.y
            self.ne = Quadtree(depth-1, Rect(x, y, w, h))
            w = self.rect.w / 2
            h = self.rect.h / 2
            x = self.rect.x + w
            y = self.rect.y + h
            self.se = Quadtree(depth-1, Rect(x, y, w, h))
            w = self.rect.w / 2
            h = self.rect.h / 2
            x = self.rect.x
            y = self.rect.y + h
            self.sw = Quadtree(depth-1, Rect(x, y, w, h))
            w = self.rect.w / 2
            h = self.rect.h / 2
            x = self.rect.x
            y = self.rect.y
            self.nw = Quadtree(depth-1, Rect(x, y, w, h))

    def insert(self, obj):
        if (not self.rect.intersect(obj.getRect())):
            return
        if (self.depth == 1):
            self.objs.append(obj)
        else:
            self.ne.insert(obj)
            self.se.insert(obj)
            self.sw.insert(obj)
            self.nw.insert(obj)

    def query(self, obj):
        inRange = list()
        if (not self.rect.intersect(obj.getRect())):
            return inRange
        if (self.depth == 1):
            for o in self.objs:
                if (obj.intersect(o)):
                    inRange.append(o)
        else:
            inRange.extend(self.ne.query(obj))
            inRange.extend(self.se.query(obj))
            inRange.extend(self.sw.query(obj))
            inRange.extend(self.nw.query(obj))
        return inRange



def ellipseMatrix(x0, y0, a, b, theta, Image, Color, XX, YY):

    a2 = a**2
    b2 = b**2
    cost = np.cos(theta)
    sint = np.sin(theta)

    Ellipse = ( ( ( (XX-x0)*cost+(YY-y0)*sint )**2 )/(a2) +
                ( ( (XX-x0)*sint-(YY-y0)*cost )**2 )/(b2) )

    #Img	 = (Ellipse < 1.0)
    #indx,indy = np.nonzero(Img == 1)
    #Image[indx,indy] = Color

    Image[Ellipse < 1.0] = Color
    return Image



def circleMatrix(x0, y0, a, Image, Color, XX, YY):

    a2 = a**2
    Ellipse = (XX-x0)**2  + (YY-y0)**2
    Image[Ellipse < a2] = Color
    return Image


def ellipseDiscard(x0, y0, a, b, theta, XX, YY, coords, mask, value):

    XXX = XX[::1,::1]
    YYY = YY[::1,::1]
    Ellipse = ( ( ( (XXX-x0)*np.cos(theta)+(YYY-y0)*np.sin(theta) )**2 )/(a**2) +
												( ( (XXX-x0)*np.sin(theta)-(YYY-y0)*np.cos(theta) )**2 )/(b**2) )




    Img = np.argwhere(Ellipse <= 1.0)

    for ind in Img:
        coords.discard((ind[0],ind[1]))
        mask[ind[0],ind[1]] = value
