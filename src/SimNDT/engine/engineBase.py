#!/usr/bin/env python
# encoding: utf-8
"""
engineBase.py

Created by Miguel Molero on 2013-10-01.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy as np
import copy

global ErrorImportCL

try:
	import pyopencl		  as	 cl
	ErrorImportCL = False
except ImportError:
	ErrorImportCL = True
	
from SimNDT.engine.infoCL  import *



class EngineBase(object):
	
	def __init__(self, _simPack, _Platform):

		self.simPack  = _simPack
		self.Platform =  _Platform
		self.n = 0

		Simulation = self.simPack.Simulation
		self.dt = np.float32(Simulation.dt)
		self.dx = np.float32(Simulation.dx)
		self.dtx = np.float32(self.dt/self.dx)
		self.ddx = np.float32(1.0/self.dx)
		self.dtdxx = self.dtx * self.ddx

		if self.Platform == "OpenCL":
			self.initCL()
		self.materialSetup()
		self.initFields()
		self.staggeredProp()
		self.applyBoundaries()
		self.sourceSetup()
		self.receiverSetup()
		self.simSetup()
		
		
	def setup_CL(self):
		pass
		
	def initCL(self):
		device   = self.simPack.Simulation.Device
		platform = self.simPack.Simulation.Platform
		
		my_device = None
		try:
			for platforms in cl.get_platforms():
				if platforms.name == platform:
					for devices in platforms.get_devices():
						if cl.device_type.to_string(devices.type)== device:
							my_device =	 devices		
		except:
			platforms  = cl.get_platforms()[0]
			my_device = platforms.get_devices()[0]
		
		if my_device is None:
			platforms  = cl.get_platforms()[0]
			my_device = platforms.get_devices()[0]
			
		print(my_device)

		self.ctx   = cl.Context([my_device])
		self.queue = cl.CommandQueue(self.ctx)
		self.mf	   = cl.mem_flags
		
		
	def materialSetup(self):
		pass
		
	def initFields(self):
		pass
		
	def receiverSetup(self):
		pass
	
	def staggeredProp(self):
		pass
		
	def applyBoundaries(self):
		pass
		
	def sourceSetup(self):
		pass
		
	def simSetup(self):
		pass
		
	def initFieldsCL(self):
		pass
	