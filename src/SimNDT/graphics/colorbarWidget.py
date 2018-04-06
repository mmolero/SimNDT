__author__ = 'Miguel Molero '


import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *

import math
import numpy as	 np
import OpenGL.GL as GL
import platform


import glumpy
import colormaps



class ColorbarWidget(QGLWidget):


	def __init__(self, parent=None, width=600, height=600):

		self._width, self._height = width, height

		QGLWidget.__init__(self, QGLFormat(QGL.SampleBuffers),parent)

		self.cmap_jet = colormaps.CMAP_JET
		self.cmap_gray = colormaps.CMAP_GRAY
		self.cmap_arcoiris = colormaps.CMAP_RAINBOW
		self.colorbar  = None


	def Show(self, cmp):
		if cmp == 0: #jet
			cmp_color = self.cmap_jet
		elif cmp == 1: #gray
			cmp_color = self.cmap_gray

		C = np.linspace(0,255,256).astype(np.float32)
		C = C.reshape((1,256))
		self.colorbar = glumpy.image.Image(C, colormap=cmp_color)
		self.colorbar.draw(x=0, y=0, z = 0, width=self._width, height=self._height)
		self.swapBuffers()


	def OnDraw(self):
		self.clear()
		if self.colorbar is not None:
			self.colorbar.draw(x=0, y=0, z = 0, width=self._width, height=self._height)



	def _clear(self):
		self.qglClearColor(QColor(230, 230, 230))

	def clear(self):
		self._clear()
		GL.glClear(GL.GL_COLOR_BUFFER_BIT)


	def initializeGL(self):
		self._clear()
		GL.glEnable(GL.GL_BLEND)
		GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
		GL.glEnable(GL.GL_TEXTURE_2D)

	def paintGL(self):
		self.makeCurrent()
		self.OnDraw()


	def resizeGL(self, width, height):

		self._width, self._height =	 width, height
		GL.glViewport(0, 0, width, height)
		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glLoadIdentity()


		if self._height==0:
			self._height=1

		if self._width==0:
			self._width=1

		GL.glOrtho(0, self._width, 0, self._height, -1, 1)
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()

		self.OnDraw()


