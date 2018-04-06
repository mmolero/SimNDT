#!/usr/bin/env python
# encoding: utf-8
"""
simulation.py

Created by Miguel Molero on 2013-09-30.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy as np
from scipy.misc import imresize
from scipy.misc import imrotate

from SimNDT.core.material import Material


c11 = 4350*4350*7750
c12 = 4350*4350*7750 - 2260*2260*7750
c22 = c11
c44 = 2260*2260*7750
pzt = Material("pzt",7750.0, c11, c12, c22, c44)



class Simulation:

    def __init__(self, TimeScale=1, MaxFreq=2, PointCycle=10, SimTime=50, Order=2, Device ="CPU"):

        self.TimeScale         = TimeScale
        self.MaxFreq           = MaxFreq
        self.PointCycle        = PointCycle
        self.SimulationTime    = SimTime

        self.dx = 0
        self.dt = 0
        self.t  = 0
        self.Order    = Order
        self.Device   = Device
        self.Platform = 0
        self.MRI = 0
        self.NRI = 0
        self.Im  = 0
        self.TapGrid   = 0
        self.Rgrid     = 0
        self.TimeSteps = 0

    def job_parameters(self, materiales, transducer):

        indVL = [mat.VL for mat in materiales if mat.VL > 400]
        indVT = [mat.VT for mat in materiales if mat.VT > 400]

        if transducer.PZT:
            indVL.append(pzt.VL)
            indVL.append(pzt.VT)


        VL	= np.array(indVL)
        VT	= np.array(indVT)
        V	= np.hstack( (VL, VT) )

        self.dx = np.float32( np.min([V]) / (self.PointCycle * self.MaxFreq) )

        if self.Order== 2:
            self.dt = 0.5 * self.TimeScale * np.float32( 0.7071 * self.dx / (	 np.max([V]) ) )
        elif self.Order == 4:
            self.dt = self.TimeScale * np.float32( 0.48 * self.dx / (	 np.max([V]) ) )


        self.TimeSteps = round(self.SimulationTime/self.dt)
        self.t = self.dt*np.arange(0,self.TimeSteps)

    def jobByUser(self, dx, dt):

        self.dx = dx
        self.dt = dt

        self.TimeSteps = round(self.SimulationTime/self.dt)
        self.t = self.dt*np.arange(0,self.TimeSteps)

    def create_numericalModel(self, scenario):

        #Spatial Scale
        Pixel_mm = float(scenario.Pixel_mm)

        Mp	= np.shape(scenario.Iabs)[0]*1e-3/Pixel_mm/self.dx
        self.Rgrid = float(Mp/np.shape(scenario.Iabs)[0])
        self.TapGrid = np.around(scenario.Tap * self.Rgrid)
        self.Im = imresize(scenario.Iabs, self.Rgrid, interp='nearest')
        self.MRI, self.NRI = np.shape(self.Im)


    def rotate_model(self, theta, scenario):
        Theta = theta * (180.0/np.pi) - 270.
        if Theta != 0:
            print ("type scenario: ", np.shape(scenario.I))
            I = imrotate(np.uint8(scenario.I), Theta, interp ='nearest')
            print ("type scenario I: ", np.shape(I))
            Iabs = scenario.applyBoundaries(I)
            self.Im = imresize(np.uint8(Iabs), self.Rgrid, interp='nearest')
            self.MRI, self.NRI = np.shape(self.Im)



    def setDevice(self,Device):
        self.Device = Device

    def setPlatform(self, Platform):
        self.Platform = Platform


    def reLoad(self, Materials, Scenario, Transducer):

        self.job_parameters(Materials, Transducer)
        self.create_numericalModel(Scenario)
