
import sys
from PySide.QtCore	import *
from PySide.QtGui import *
from PySide.QtOpenGL import *

import math
import numpy as	 np
import OpenGL.GL as GL
import platform


import glumpy
import colormaps

import SimNDT.gui.HelperMethods  as HelperMethods


def mapValue(data,in_min,in_max,out_min,out_max):
	return (data-in_min)*(out_max-out_min)/(in_max-in_min) + out_min



class RefreshZoom(QObject):

	zoomed = Signal(int)

	def __init__(self):
		QObject.__init__(self)

	def zoom(self, value):
		self.zoomed.emit(value)



class GLWidget(QGLWidget):
	
	
	def __init__(self, parent=None, width=600, height=600):

		self.parent = parent
		self._width, self._height = width, height
		QGLWidget.__init__(self, QGLFormat(QGL.SampleBuffers), parent)

		self.setAttribute(Qt.WA_NoSystemBackground)
		self.refreshZoom = RefreshZoom()
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.showContextMenu)




		self.cmap_jet = colormaps.CMAP_JET
		self.cmap_gray = colormaps.CMAP_GRAY
		self.cmap_arcoiris = colormaps.CMAP_RAINBOW


		self._Starting = False
		self.Enable = False
		
		self._x = self._width/2.0
		self._y	= self._height/2.0
		self._zoom = 0.3
		
		self.Offset = QPoint()
		self.ActualPosition = QPoint()
		self.DragStart = QPoint()
		self.newOffset= QPoint()
		self._dx = 0
		self._dy = 0
		
		self.image = None
		self._ImageSim = False
		
		self.EnableTransducers = False
		self._ABS = False

		self.cmap = self.cmap_jet
		
	def init(self):
		
		self.resizeGL(self._width,self._height)
		self.initializeGL()

	def disable(self):
		self._Starting	= False


	def showContextMenu(self, pos):

		menu = QMenu()
		HelperMethods.addActions(menu, self.parent.actionAdd_Ellipse)
		HelperMethods.addActions(menu, self.parent.actionAdd_Rectangle)
		menu.exec_(self.mapToGlobal(pos))




	def setColormap(self,value):

		if value == 0:
			self.cmap = self.cmap_jet
		elif value == 1:
			self.cmap = self.cmap_gray

	def setImage(self,I, DB = 60):
		
		self.DB   = DB
		self.time = 0		
		
		self._Starting	= True
		I = np.float32(I)
		self.Z		=  I
		self.image	= []
		self.image	= glumpy.image.Image(self.Z, interpolation='bilinear',
												 colormap=self.cmap,
												 vmin= -self.DB, vmax=0)

		C = np.linspace(-self.DB,0,256).astype(np.float32)
		C = C.reshape((1,256))
		self.colorbar = glumpy.image.Image(C, colormap=self.cmap)
		
		self._ImageSim = True
		self.values_text = np.linspace(-self.DB,0,10, endpoint=True)
		self.tick  = [mapValue(i,-self.DB,0,0,self._width-10) for i in self.values_text]
		
	
	def updateWithImage(self,I, time):
		self.M,self.N = np.shape(I)
		self.time = time
		self.Z[...] =  I
		self.image.update()
		self.updateGL()
	

	def imshow(self, I):
		
		self._ImageSim = False
		I = np.float32(I)
		self.M, self.N = np.shape(I)
		self.image	  = []
		self.image = glumpy.image.Image(I, interpolation="nearest" ,colormap=self.cmap_jet, vmin= 0.0, vmax=255)	
		C = np.linspace(0,255,256).astype(np.float32)
		C = C.reshape((1,256))
		self.colorbar = glumpy.image.Image(C, colormap=self.cmap_jet)
		self.values_text = [0,40,80,120,160,200,240]
		self.tick  = [mapValue(i,0,255,0,self._width-10) for i in self.values_text]

		self.updateGL() 
		

	def materials(self):

		m = 40*np.ones((30,30)).astype(np.float32)
		self.mat = glumpy.image.Image(m, colormap=self.cmap_jet, vmin=0, vmax=255)

	def updateMaterials(self):

		self.mat.draw(x=self._width-100, y=self._height-50, z=0, width= 10, height=10)
		self.qglColor(QColor(0,0,0))
		self.renderText(self._width-90, 50, "aluminium")



	def _clear(self):
		self.qglClearColor(QColor(230, 230, 230))
	
	def clear(self):
		self._clear()
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)
		
		
	def clearUpdate(self):
		self.image = None
		self.updateGL()
	
	def initializeGL(self):
		self._clear()
		GL.glDisable(GL.GL_BLEND)
		#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		#glEnable(GL_TEXTURE_2D)
		
	def paintGL(self):
		self.makeCurrent()
		self.OnDraw()
		
	def setupZoom(self, value):
		self._zoom =  0.3*value/100.0
		
	def setZoom(self,value):
		self._zoom =  0.3*value/100.0
		self.updateGL()
		
	def getZoom(self):
		return 100*self._zoom/0.3


	def wheelEvent(self, event):
		numDegrees = event.delta() / 8
		numSteps = numDegrees / 15.0
		self.setZoom(numSteps + self.getZoom())
		self.refreshZoom.zoom(self.getZoom())



	def drawAxis(self):

		GL.glDisable(GL.GL_TEXTURE_2D)
		GL.glDisable(GL.GL_BLEND)

		GL.glLineWidth(1)
		GL.glColor3f(0.0, 0.0, 0.0)


		y0  = 30
		y1  = y0 + 60
		_x0 = 30
		_y0 = self._height-y0
		_x1 = _x0 + 60
		_y1 = _y0 - 60


		GL.glPointSize(7)
		GL.glBegin(GL.GL_POINTS)
		GL.glVertex2f(_x0,_y0)
		GL.glEnd()

		GL.glBegin(GL.GL_LINES)
		GL.glVertex2f(_x0, _y0)
		GL.glVertex2f(_x0, _y1)
		GL.glVertex2f(_x0, _y0)
		GL.glVertex2f(_x1 ,_y0)
		GL.glEnd()

		_w = 5
		GL.glBegin(GL.GL_TRIANGLES)
		GL.glVertex2f(_x0 +_w, _y1)
		GL.glVertex2f(_x0 -_w, _y1)
		GL.glVertex2f(_x0,_y1 -_w)
		GL.glEnd()

		GL.glBegin(GL.GL_TRIANGLES)
		GL.glVertex2f(_x1, _y0+_w)
		GL.glVertex2f(_x1, _y0-_w)
		GL.glVertex2f(_x1+_w,_y0)
		GL.glEnd()

		GL.glDisable(GL.GL_BLEND)
		GL.glColor3f(0.0, 0.0, 0.0)
		self.renderText(_x1 + 2*_w, y0+_w, "X")
		self.renderText(_x0-_w, y1 + 4*_w, "Y")

		
		
	def OnDraw(self):

		self.clear()


		if self.image:
			x = self._width/2.0  - self.N*self._zoom/2.0
			y = self._height/2.0 - self.M*self._zoom/2.0
			
			self.image.draw(x=x, y=y,z=0, width= self.N*self._zoom , height= self.M*self._zoom)	
			self.colorbar.draw(x=0, y=0, z = 0, width=self._width, height=20 )



			if self._ImageSim:
				self.tick  = [mapValue(i,-self.DB,0,0,self._width-10) for i in self.values_text]
				x0 = self._width/2.0  - self.N*self._zoom*0.1  
				y0 = self._height/2.0 - self.M*self._zoom/2.0 - self.M*self._zoom*0.02 
				self.qglColor(QColor(0,0,0))
				self.renderText(x0, y0, " time = %.2f %ss"%(self.time, unichr(956)))
				
			else:
				self.tick  = [mapValue(i,0,255,0,self._width-10) for i in self.values_text]
				
		
			self.qglColor(QColor(0,0,0))
			for i, t in zip(self.values_text,self.tick):
				if self._ImageSim:
					self.renderText(int(t), self._height-20, str(int(i))+" dB")
				else:
					self.renderText(int(t), self._height-20, str(int(i)))
					

			self.drawAxis()

			if self.EnableTransducers:
				GL.glDisable(GL.GL_TEXTURE_2D)
				GL.glDisable(GL.GL_BLEND)
				self.drawTransducers()
				
				
				
		
	def setTransducers(self, X,Y):
		self.XL = X
		self.YL = Y
		
	def drawTransducers(self):
		
		x = self._width/2.0   - self.N*self._zoom/2.0 + self.XL*self._zoom 
		y = self._height/2.0  - self.M*self._zoom/2.0 + self.YL*self._zoom
		GL.glLineWidth(5);
		GL.glColor3f(0.0, 0.0, 0.0);
		for j in range(np.size(x,1)):
			for i in range(np.size(x,0)-1):
				GL.glBegin(GL.GL_LINES);
				GL.glVertex2f(x[i,j],  y[i,j])
				GL.glVertex2f(x[i+1,j],y[i+1,j]);
				GL.glEnd();
				
		
		
	def resizeGL(self, width, height):
		
		self._width, self._height =	 width, height
		GL.glViewport(0, 0, width, height);
		GL.glMatrixMode(GL.GL_PROJECTION);
		GL.glLoadIdentity();
		
		
		if self._height==0:
			self._height=1;
			
		if self._width==0:
			self._width=1;
		
		GL.glOrtho(0, self._width, 0, self._height, -1, 1)
		GL.glMatrixMode(GL.GL_MODELVIEW);
		GL.glLoadIdentity();

		self.OnDraw()
		

		

	def mousePressEvent(self, event):
		self.DragStart      = QPoint(event.pos())
		
	def mouseMoveEvent(self, event):
		
		self.ActualPosition = QPoint(event.pos())
		if event.buttons() & Qt.LeftButton:
				
			self.newOffset  = self.Offset
			x  =  self.ActualPosition.x()-self.DragStart.x()
			y  =  self.ActualPosition.y()-self.DragStart.y()  
			self.Offset = QPoint(x,y)
			self._dx = self.Offset.x()
			self._dy = self.Offset.y() 
			
			self.updateGL()

		

	



