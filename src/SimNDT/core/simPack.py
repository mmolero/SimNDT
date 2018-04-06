#!/usr/bin/env python
# encoding: utf-8
"""
simPack.py

Created by Miguel Molero on 2013-10-01.
Copyright (c) 2013 MMolero. All rights reserved.
"""

class SimPack:
	
	def __init__(self, scenario,  materials, boundary, inspection, source, transducers, signal, simulation):
		
		self.Boundary    = boundary
		self.Inspection  = inspection
		self.Source      = source
		self.Materials   = materials
		self.Transducers = transducers
		self.Simulation  = simulation
		self.Scenario    = scenario
		self.Signal      = signal
		