#!/usr/bin/env python
# encoding: utf-8
"""
inspectionMethods.py

Created by Miguel Molero on 2013-09-26.
Copyright (c) 2013 MMolero. All rights reserved.
"""

from math import sin, cos, sqrt, pi
import numpy as np

import SimNDT.core.inspectionSetup as Inspection
import copy

class Source:
	def __init__(self):
		self.Longitudinal = True
		self.Shear        = False
		self.Pressure    = True
		self.Displacement = False



class SingleLaunch:
	
	@classmethod
	def view(cls, M, N, Pixel_mm, Theta, transducer):
		x2 = np.zeros((2,),dtype=np.float32)
		y2 = np.zeros((2,),dtype=np.float32)

		Ntheta	=  np.size(Theta,0)
		D_T = np.around(M/2.)

		if transducer.PointSource:
			SizePixel = 0.5
		else:
			SizePixel = np.around( 0.5 * Pixel_mm * transducer.Size )

		Location = transducer.Location

		if Location == "Top":

			x2  = M/2.  + (D_T)*np.sin(Theta)
			y2  = N/2.  + (D_T)*np.cos(Theta)
		
			X0	= np.around(M/2.)
			Y0	= np.around(N/2.)

			XL, YL = Inspection.setEmisor(Theta, SizePixel, x2, y2, X0, Y0)
			YL		+= (np.around(transducer.CenterOffset * Pixel_mm ))
			XL[:,0] += (np.around(transducer.BorderOffset * Pixel_mm ))
			XL[:,1] -= (np.around(transducer.BorderOffset * Pixel_mm ))
			XL  = np.fliplr(XL)


		elif Location == "Left":

			x2  = M/2.  + (D_T)*np.sin(Theta)
			y2  = N/2.  + (D_T)*np.cos(Theta)

			X0	= np.around(M/2.)
			Y0	= np.around(N/2.)

			XL, YL = Inspection.setEmisor(Theta, SizePixel, x2, y2, X0, Y0)
			XL	  += (np.around(transducer.CenterOffset * Pixel_mm ))

			YL[:,0] += (np.around(transducer.BorderOffset * Pixel_mm ))
			YL[:,1] -= (np.around(transducer.BorderOffset * Pixel_mm ))
			YL  = np.fliplr(YL)


		return XL, YL
	
	
	def	setInspection(self, Scenario, Transducer, Simulation):
		"""
		set Inspection on numerical model
		"""
		MRI, NRI = Simulation.MRI, Simulation.NRI
		TapGrid = Simulation.TapGrid
		Rgrid   = Simulation.Rgrid
		M       = np.shape(Scenario.Iabs)[0] *Rgrid
		N       = np.shape(Scenario.Iabs)[1] *Rgrid
		M2      = M/ 2.0
		N2      = N/ 2.0
		
		x2 = np.zeros((2,),dtype=np.float32)
		y2 = np.zeros((2,),dtype=np.float32)
		Ntheta	=  np.size(self.Theta,0)
		
		X0	   =  np.around((MRI)/2.0)
		Y0	   =  np.around((NRI)/2.0)
		x2[0]  =      X0  +   (M2-TapGrid[0])*np.sin(self.Theta[0])+1 


		if Transducer.Location == "Top":

			if self.Method  == "PulseEcho":
				x2[1]  =  x2[0]
			else:
				x2[1]  =  X0  +  (M2-TapGrid[1])*np.sin(self.Theta[1])-1
			y2[:]  = (NRI-TapGrid[2]-TapGrid[3])/2.0 + TapGrid[2]


		elif Transducer.Location == "Left":

			if self.Method  == "PulseEcho":
				y2[1]  =  y2[0]
			else:
				y2[1]  =  Y0  +  (M2-TapGrid[1])*np.sin(self.Theta[1])-1

			x2[:]  = (NRI-TapGrid[2]-TapGrid[3])/2.0 + TapGrid[2]


		if Transducer.PointSource:
			Transducer.SizePixel = 0.5
		else:
			Transducer.SizePixel =  np.around( 0.5 * Scenario.Pixel_mm * Transducer.Size * Rgrid )
		
		XL, YL     = Inspection.setEmisor(self.Theta, Transducer.SizePixel, x2, y2, X0, Y0)
		XL, YL, IR = Inspection.centerOffset(XL, YL, self.Theta, Scenario, Transducer, Rgrid)
		XL, YL     = Inspection.borderOffset(XL, YL, Scenario, Transducer, Rgrid)
			
		self.XL = XL.copy()
		self.YL = YL.copy()
		self.IR = IR.copy()
		
		
	def getReceivers(self, T):
		return Inspection.getReceivers(self.XL, self.YL, self.IR, T, False)



class Transmission(SingleLaunch):

	def __init__(self,Location="Top"):	
		self.Name  = "Transmission"
		self.Method = "Transmission"
		self.Location = Location



		if Location=="Top":
			self.Theta = [270.0*pi/180.0, 90.0*pi/180.0]
		elif Location == "Left":
			self.Theta = [180.0*pi/180.0, 0.0*pi/180.0]

		

class PulseEcho(SingleLaunch):

	def __init__(self,Location="Top"):	
		self.Name  = "PulseEcho"
		self.Method = "PulseEcho"
		self.Location = Location
		if Location=="Top":
			self.Theta = [270.0*pi/180.0, 270*pi/180.0]
		elif Location=="Left":
			self.Theta = [180.0*pi/180.0, 0.0*pi/180.0]
			
		
	
class LinearScan(SingleLaunch):

	def __init__(self, ini=-10, end=10, step=1, 
	                   Location="Top", Method = "Transmission",Theta = [270.0*pi/180.0, 90.0*pi/180.0]):
		
		self.Name  = "LinearScan"
		self.Location = Location
		Num = np.size(  np.arange(ini,end,step))
		self.ScanVector = np.linspace(ini, end, Num+1, endpoint=True)
		self.ScanVectorString = "(%g,%g,%g)"%(ini,end,step)
		self.Method = Method
		self.Theta  = Theta
		

		
		
		
		
class Tomography:
	
	def __init__(self,ProjectionStep=45,DiameterRing=50,OneProjection=False):
		
		self.Name = "Tomography"
		self.Method = "Transmission"
		self.DiameterRing	  = DiameterRing
		self.ProjectionStep	  = ProjectionStep 
		self.OneProjection	  = OneProjection
		self.Theta			  = np.arange(270,-90.0, -self.ProjectionStep)*(pi/180.0)
		
	
	@staticmethod
	def view(M, N, DiameterRing, Pixel_mm, Theta, transducer):
	
		x2 = np.zeros((2,),dtype=np.float32)
		y2 = np.zeros((2,),dtype=np.float32)

		Ntheta	=  np.size(Theta,0)
		D_T =  np.around(DiameterRing*Pixel_mm/2.)
		
		x2  = M/2.  + (D_T)*np.sin(Theta)
		y2  = N/2.  + (D_T)*np.cos(Theta)
		
		X0	= np.around(M/2.)
		Y0	= np.around(N/2.)

		if transducer.PointSource:
			SizePixel = 0.5
		else:
			SizePixel = np.around( 0.5 * Pixel_mm * transducer.Size )
			
		XL, YL = Inspection.setEmisor(Theta, SizePixel, x2, y2, X0, Y0)

		return XL, YL
	


	def	setInspection(self, Scenario, Transducer, Simulation):
		"""
		set Inspection on numerical model
		"""
		MRI, NRI = Simulation.MRI, Simulation.NRI
		TapGrid = Simulation.TapGrid
		Rgrid   = Simulation.Rgrid
		M       = np.shape(Scenario.Iabs)[0] *Rgrid
		N       = np.shape(Scenario.Iabs)[1] *Rgrid
		M2      = M/ 2.0
		N2      = N/ 2.0
		Pixel_mm = Scenario.Pixel_mm

		Ntheta	=  np.size(self.Theta,0)
		DR	   =  np.around(self.DiameterRing*Pixel_mm*Rgrid/2.)

		X0	   =  TapGrid[0] + (Scenario.M/2.0)*Rgrid
		Y0	   =  TapGrid[2] + (Scenario.N/2.0)*Rgrid
		x2     =  X0  +  (DR)*np.sin(self.Theta) 
		y2     =  Y0  +  (DR)*np.cos(self.Theta)

		if Transducer.PointSource:
			Transducer.SizePixel = 0.5
		else:
			Transducer.SizePixel =  np.floor( 0.5 * Scenario.Pixel_mm * Transducer.Size * Rgrid )

		XL, YL = Inspection.setEmisor(self.Theta, Transducer.SizePixel, x2, y2, X0, Y0)
		XL, YL, IR = Inspection.centerOffset(XL, YL, self.Theta, Scenario, Transducer, Rgrid)
			
			
		self.XL = XL.copy()
		self.YL = YL.copy()
		self.IR = IR.copy()

	
	def getReceivers(self, T):
		return Inspection.getReceivers(self.XL, self.YL, self.IR, T, False)
		
		
		
		