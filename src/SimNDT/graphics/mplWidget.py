#!/usr/bin/env python
# encoding: utf-8
"""
pltWidget.py

Created by Miguel Molero on 2013-09-20.
Copyright (c) 2013 MMolero. All rights reserved.
"""

from __future__ import unicode_literals
import sys, os, random

os.environ['QT_API'] = 'pyside'

import matplotlib
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


from PySide.QtGui	import *
import numpy as np


class NavigationToolbar(NavigationToolbar):
    # only display the buttons we need
	print (sys.platform)

class MplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):

		self.fig  = Figure(figsize=(width, height), dpi=dpi)
		self.ax   = self.fig.add_subplot(111)

		self.fig.patch.set_facecolor('white')

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
		FigureCanvas.updateGeometry(self)
		self.setMinimumSize(250,250)


class PlotDialog(QDialog):
	

	def __init__(self, parent=None, width=6, height=5, dpi=100):
		super(PlotDialog,self).__init__(parent)
		self.parent = parent
		
		self.mpl = MplCanvas(self, width=width, height=height, dpi=dpi)
		self.mpl_toolbar = NavigationToolbar(self.mpl, self)
		
		layout = QVBoxLayout()
		layout.addWidget(self.mpl)
		layout.addWidget(self.mpl_toolbar,0)
		
		self.setLayout(layout)
		
		
		self.mpl.fig.patch.set_facecolor('white')
		
		for item in ([self.mpl.ax.title, self.mpl.ax.xaxis.label, self.mpl.ax.yaxis.label] +
		             self.mpl.ax.get_xticklabels() + self.mpl.ax.get_yticklabels()):
		    item.set_fontsize(10)
		
		
		self.setWindowFlags(self.windowFlags() )
		self.setWindowTitle(self.tr("Plot Inspection"))
		self.setMinimumSize(250,250)
		self.setMaximumSize(2000,1500)
		
		
		
class PlotInline(QDialog):
	
	def __init__(self, parent=None):
		super(PlotInline, self).__init__(parent)
		
		self.mpl = MplCanvas(self, width=6, height=2, dpi=100)
		layout = QVBoxLayout()
		layout.addWidget(self.mpl)
		self.setLayout(layout)
		
	
		self.mpl.fig.patch.set_facecolor('lightgray')
		for item in ([self.mpl.ax.title, self.mpl.ax.xaxis.label, self.mpl.ax.yaxis.label] +
		             self.mpl.ax.get_xticklabels() + self.mpl.ax.get_yticklabels()):
			item.set_fontsize(10)
			#item.set_color('white')
			
			
		#self.mpl.ax.spines['bottom'].set_color('white')
		#self.mpl.ax.spines['top'].set_color('white')
		#self.mpl.ax.spines['left'].set_color('white')
		#self.mpl.ax.spines['right'].set_color('white')
		
		self.setWindowFlags(self.windowFlags() )
		self.setWindowTitle(self.tr("Receiver Signal"))
		self.setMinimumSize(250,250)
		self.setMaximumSize(2000,1500)				
		self.resize(900,350)
		
		
	def init(self, sig, SimulationTime):
		lenght = np.size(sig[:,0])
		self.time = np.linspace(0,SimulationTime, lenght)*1e6
		
		self.data = list()
		self.plot, = self.mpl.ax.plot([], [], color='green', linewidth=2)
		
		self.min = -0.01
		self.max =  0.01		
		
		self.mpl.ax.patch.set_facecolor('lightgray')
		
		self.mpl.ax.set_ylim(self.min, self.max)
		self.mpl.ax.set_xlim(0, self.time[-1])
		
		self.mpl.ax.grid(True, color='black')
		self.mpl.ax.set_title("Time Signal", fontsize = 10)
		self.mpl.ax.set_xlabel("Time ($\mu$s)")
		self.mpl.ax.set_ylabel("Amplitude")

	def update(self, value):
		self.data.append(value)
		N = len(self.data)
		self.plot.set_data(self.time[0:N], self.data)
		vmin = np.min([np.min(self.data),self.min]) 
		vmax = np.max([np.max(self.data), self.max])
		self.mpl.ax.set_ylim(vmin,vmax)
		self.mpl.draw()
		

