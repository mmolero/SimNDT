cimport cython
import math

import numpy as np
cimport numpy as np

cdef extern from "math.h":
    double sin(double x)
    double cos(double x)
    double sqrt(double x)

DEF pi = 3.141592


cdef class Rect:
    cdef int x, y, w, h
    def __init__(self,  int x,  int y,  int w,  int h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    cpdef collide(self, int x, int y):
        return ((self.x <= x <= self.x + self.w) and
                 (self.y <= y <= self.y + self.h))

    cpdef intersect(self, Rect rect):
        return ((self.x < rect.x + rect.w) and (rect.x < self.x + self.w) and
                (self.y < rect.y + rect.h) and (rect.y < self.y + self.h))


cdef class Object:
    cdef int x0, y0, w, h

    cpdef getRect(self):
        return Rect(self.x0, self.y0, self.w, self.h)


cdef class Circle(Object):
    cdef:
        int x, y,  r
    def __init__(self, int x, int y, int r):
        self.x = x
        self.y = y
        self.r = r
        self.x0 = self.x - self.r
        self.y0 = self.y - self.r
        self.w =  2 * self.r
        self.h = 2 * self.r

    cpdef area(self):
        return pi * self.r**2

    cpdef distance(self, int x, int y):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2)

    cpdef collide(self, x, y):
        return (self.distance(x, y) <= self.r)

    cpdef intersect(self, Circle circle):
        if (self.distance(circle.x, circle.y) <= self.r + circle.r):
            return True
        else:
            return False



cdef class Ellipse2(Object):

    cdef public int x, y, a, b
    cdef public double theta
    cdef double k1_, k2_, k3_

    def __init__(self, int x, int y, int da, int db, double theta):
        cdef double c, s

        if (da > db):
            a = da
            b = db
        else:
            a = db
            b = da

        c = cos(theta)
        s = sin(theta)

        #Find k1_, k2_, k3_ - define when a point x,y is on the ellipse
        k1_ = sqr(c / a) + sqr(s / b);
        k2_ = 2 * s * c * ((1 / sqr(a)) - (1 / sqr(b)));
        k3_ = sqr(s / a) + sqr(c / b);








cdef class Ellipse(Object):

    cdef int _x, _y, _a, _b
    cdef double _theta
    cdef Rect rect

    def __init__(self, int x, int y, int a, int b, double theta):

        cdef double xmin, xmax, ymin, ymax
        cdef np.ndarray[np.float32_t, ndim=1] t, xx, yy


        self._x = x
        self._y = y
        self._a = a
        self._b = b
        self._theta = theta

        t	= np.linspace(0,2*pi,20, endpoint=True, dtype=np.float32)
        xx	= self._x  + self._a * np.cos(t)
        yy	= self._y  + self._b * np.sin(t)

        xmin = np.min(xx)
        xmax = np.max(xx)
        ymin = np.min(yy)
        ymax = np.max(yy)

        self.w = int(xmax-xmin)
        self.h = int(ymax-ymin)

        self.x0 = int((xmax+xmin)/2.0)
        self.y0 = int((ymax+ymin)/2.0)

        self.rect = self.getRect()

    cpdef x(self):
        return self._x

    cpdef y(self):
        return self._y

    cpdef a(self):
        return self._a

    cpdef b(self):
        return self._b

    cpdef theta(self):
        return self._theta


    cpdef area(self):
        return pi * self._a * self._b


    cpdef intersect2(self, Ellipse ellipse):

        return ( (np.abs(self.rect.x - ellipse.rect.x) * 2.0 < (self.rect.w + ellipse.rect.w) ) and
               (np.abs(self.rect.y - ellipse.rect.y) * 2.0 < (self.rect.h + ellipse.rect.h)) )


    cpdef intersect(self, Ellipse ellipse):

        cdef double c, Mb, d, d1, d2, cost, sint
        cdef double a2, b2, tmp

        a2 = ellipse.a()**2
        b2 = ellipse.b()**2

        cost  =	 cos(ellipse.theta())
        sint  =	 sin(ellipse.theta())


        tmp = ( ( ( (ellipse.x() - self.x())* cost + ( ellipse.y() - self.y())* sint )**2 )/(a2) +
                ( ( (ellipse.x() - self.x())* sint - ( ellipse.y() - self.y())* cost )**2 )/(b2) )

        if tmp <= 1.0:
            return True


        c =	sqrt(self._a**2 - self._b**2)
        cost  =	 c * cos(self._theta)
        sint  =	 c * sin(self._theta)

        d1	= (ellipse.x() - self._x - cost)**2 + (ellipse.y() - self._y - sint)**2
        d1	= sqrt(d1)
        d2	= (ellipse.x() - self._x + cost)**2 + (ellipse.y() - self._y + sint)**2
        d2	= sqrt(d2)
        d	= sqrt( (self._x-ellipse.x())**2 + (self._y-ellipse.y())**2 )

        if self._a >= 8*ellipse.a():
            Mb	= 0.15*self._a + ellipse.a()

        elif ellipse.a() >= 8*self._a:
            Mb	= self._a + 0.15*ellipse.a()

        else:
            Mb	= self._a + ellipse.a()

        if	(d1+d2 <= Mb) or (d <= Mb):
            return True

        return False


cdef class Quadtree:
    cdef Quadtree ne, se, sw, nw
    cdef Rect rect
    cdef int depth
    cdef list objs

    def __init__(self, int depth, Rect rect):
        cdef int w, h, x, y

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

    def insert(self, Object obj):

        if (not self.rect.intersect(obj.getRect())):
            return
        if (self.depth == 1):
            self.objs.append(obj)
        else:
            self.ne.insert(obj)
            self.se.insert(obj)
            self.sw.insert(obj)
            self.nw.insert(obj)

    def query(self, Object obj):

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




def ellipseMatrix(int x0, int y0, int a, int b, double theta,
                  np.ndarray[np.int32_t, ndim=2] Image, int Color,
                  np.ndarray[np.int32_t, ndim=2] XX,  np.ndarray[np.int32_t, ndim=2] YY):

    cdef int a2,b2
    cdef double cost, sint

    a2 = a**2
    b2 = b**2
    cost = cos(theta)
    sint = sin(theta)

    Ellipse = ( ( ( (XX-x0)*cost+(YY-y0)*sint )**2 )/(a2) +
                ( ( (XX-x0)*sint-(YY-y0)*cost )**2 )/(b2) )

    Image[Ellipse < 1.0] = Color
    return Image