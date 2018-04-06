from PySide.QtCore import *
from PySide.QtGui import *
import SimNDT.gui.HelperMethods  as HelperMethods

import numpy as np
import matplotlib.cm  as cm

jet	= cm.jet(range(0,256))
r,g,b,a = jet[:,0], jet[:,1], jet[:,2],jet[:,3]
cmap_jet =  [QColor(r_*255, g_*255, b_*255).rgb() for r_,g_,b_ in zip(r,g,b)]

jet = cm.gray(range(0,256))
r,g,b,a = jet[:,0], jet[:,1], jet[:,2],jet[:,3]
cmap_gray =  [QColor(r_*255, g_*255, b_*255).rgb() for r_,g_,b_ in zip(r,g,b)]


def mapValue(data,in_min,in_max,out_min,out_max):
    return (data-in_min)*(out_max-out_min)/(in_max-in_min) + out_min

def array2qimage(data, vmin = 0.0, vmax = 255.0, cmap=cmap_jet):
    """Convert the 2D numpy array `gray` into a 8-bit QImage with a gray
    colormap.  The first dimension represents the vertical image axis.

    Note
    ----
    Main Idea taken from http://kogs-www.informatik.uni-hamburg.de/~meine/software/vigraqt/qimage2ndarray.py
    http://pointsofsail.org/displaying-a-2-d-numpy-array-in-pyside/

    ATTENTION: This QImage carries an attribute `ndimage` with a
    reference to the underlying numpy array that holds the data. On
    Windows, the conversion into a QPixmap does not copy the data, so
    that you have to take care that the QImage does not get garbage
    collected (otherwise PyQt/PySide will throw away the wrapper, effectively
    freeing the underlying memory - boom!).
    """

    im = data.copy()

    if im.ptp()==0:
        im = np.uint8(im)
    else:
        im = np.uint8(mapValue(im,vmin,vmax, 0.0,255.0))

    qimage = QImage(im.data, im.shape[1], im.shape[0], im.shape[1], QImage.Format_Indexed8)
    qimage.ndarray = im
    qimage.setColorTable(cmap)
    return qimage


class RefreshZoom(QObject):
    zoomed = Signal(int)
    def __init__(self):
        QObject.__init__(self)

    def zoom(self, value):
        self.zoomed.emit(value)





class GraphicView(QGraphicsView):

    def __init__(self, parent, *args, **kwargs):
        super(GraphicView, self).__init__(*args, **kwargs)

        self.parent = parent
        #self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setFrameStyle(QFrame.NoFrame)
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        #Aself.setRenderHint(QPainter.SmoothPixmapTransform)

        self._zoom = 1
        self.refreshZoom = RefreshZoom()

        self.scene = QGraphicsScene(0,0, 1000,1000)
        self.setScene(self.scene)

        self.pixmapItem = None
        self.textItem = None
        self.colormapBarItem = None

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        menu = QMenu()
        HelperMethods.addActions(menu, self.parent.actionAdd_Ellipse)
        HelperMethods.addActions(menu, self.parent.actionAdd_Rectangle)
        menu.exec_(self.mapToGlobal(pos))


    def setupZoom(self, value):
        self.setZoom(value)


    def setZoom(self, value):
        self._zoom = 0.3*value/100.0
        scale = self._zoom/self.transform().m11()
        self.scale(scale, scale)

    def getZoom(self):
        return self._zoom*100.0/0.3


    def wheelEvent(self, event):
        #angleDelta
        numSteps = event.delta() / 8.0 /15.0
        self.setZoom( self.getZoom() + numSteps )
        scale = self._zoom/self.transform().m11()
        self.scale(scale,scale)
        self.refreshZoom.zoom( int (self.getZoom() ))


    def imshow(self, I):

        self.clearUpdate()
        qimage = array2qimage(I)

        if self.pixmapItem is None:
            self.pixmapItem = self.scene.addPixmap(QPixmap.fromImage(qimage))
            self.pixmapItem.setFlags(QGraphicsItem.ItemIsMovable)

        else:
            self.pixmapItem.setPixmap(QPixmap.fromImage(qimage))


        self.drawColormapBar()
        self.drawAxis()

        qimage = None

        pixmap = self.pixmapItem.pixmap()
        w, h = pixmap.width(), pixmap.height()
        self.scene.setSceneRect(0,0,w,h)


    def drawAxis(self):

        line1 = QPolygonF()
        line1.append(QPointF(0,-10))
        line1.append(QPointF(0,60))
        line2 = QPolygonF()
        line2.append(QPointF(0,-10))
        line2.append(QPointF(60,-10))
        triangle1 = QPolygonF()
        triangle1.append(QPointF( 10,60))
        triangle1.append(QPointF(-10,60))
        triangle1.append(QPointF(0,65))
        triangle1.append(QPointF(10,60))
        triangle2 = QPolygonF()
        triangle2.append(QPointF( 60,-20))
        triangle2.append(QPointF( 60, 0))
        triangle2.append(QPointF(65,-10))
        triangle2.append(QPointF(60,-20))

        path = QPainterPath()
        path.addPolygon(line1)
        path.addPolygon(line2)
        path.addPolygon(triangle1)
        path.addPolygon(triangle2)

        pathItem = QGraphicsPathItem(self.pixmapItem)
        pathItem.setPath(path)
        pathItem.moveBy(-40,-40)

    def drawColormapBar(self):

        pixmap = self.pixmapItem.pixmap()
        w, h = pixmap.width(), pixmap.height()
        C = np.linspace(0,255, w, endpoint=True).astype(np.uint8)
        C = np.tile(C, (40, 1))
        Cqimage = array2qimage(C)

        if self.colormapBarItem is None:
            self.colormapBarItem = QGraphicsPixmapItem(self.pixmapItem)
            self.colormapBarItem.setPixmap(QPixmap.fromImage(Cqimage))
            self.colormapBarItem.setPos(0,h+20)
            self.drawTicksColormapBar(w,h)

        Cqimage = None

    def drawTicksColormapBar(self, w, h):

        font = QFont()
        font.setPixelSize(w/20)
        font.setBold(False)
        font.setFamily("Calibri")

        values_text = [0,40,80,120,160,200,240]
        tick = [mapValue(i,0, 255, 0, w-15) for i in values_text]
        for item, pos in zip(values_text, tick):
            text = QGraphicsTextItem(self.pixmapItem)
            text.setPlainText("%s"%item)
            text.setFont(font)
            text.setPos(pos, h+60)

    def clearUpdate(self):

        self.scene.clear()
        self.viewport().update()
        self.pixmapItem = None
        self.textItem = None
        self.colormapBarItem = None

    def setImage(self, I, DB=60):
        vmin, vmax = -DB, 0

        self.clearUpdate()
        I[ I <-DB] = -DB

        qimage = array2qimage(I, vmin = vmin, vmax = vmax, cmap=self.cmap)
        self.pixmapItem = self.scene.addPixmap(QPixmap.fromImage(qimage))
        #pixmap = self.pixmapItem.pixmap()
        #self.pixmapItem.setOffset(-pixmap.width()/2.0,-pixmap.height()/2.)
        self.pixmapItem.setGraphicsEffect(QGraphicsBlurEffect())
        self.pixmapItem.setFlags(QGraphicsItem.ItemIsMovable)
        qimage = None


        if self.textItem is None:
            pixmap = self.pixmapItem.pixmap()
            w = pixmap.width()
            font = QFont()
            font.setPixelSize(w/25)
            font.setBold(False)
            font.setFamily("Calibri")

            self.textItem = QGraphicsTextItem(self.pixmapItem)
            self.textItem.setPlainText("time:")
            self.textItem.setPos(0,-(20+ w/25) )
            self.textItem.setFont(font)



    def updateWithImage(self, I, time, DB=60):

        vmin, vmax = -DB, 0
        I[ I <-DB] = -DB
        qimage = array2qimage(I, vmin = vmin, vmax = vmax, cmap=self.cmap)
        self.pixmapItem.setPixmap(QPixmap.fromImage(qimage))
        qimage = None
        self.textItem.setPlainText("time: %0.2f %ss"%(time,(956)) )


    def setColormap(self,value):
        if value == 0:
            self.cmap = cmap_jet
        elif value == 1:
            self.cmap = cmap_gray