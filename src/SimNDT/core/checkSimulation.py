#!/usr/bin/env python
# encoding: utf-8
"""
checkSimulation.py

Created by Miguel Molero on 2013-10-04.
Copyright (c) 2013 MMolero. All rights reserved.
"""

import numpy as np
import copy

from SimNDT.core.constants import *
from SimNDT.core.boundary import Boundary


def boundaries(Scenario, Boundaries):
	if np.size(Scenario.Iabs) == 1:
		names = ["Top","Bottom", "Left", "Right"]
		Boundaries = [Boundary(name, BC=BC.AirLayer, size=0) for name in names]

	return Boundaries



def boundariesReLoad(Scenario, Materials, Boundaries, Transducer, Inspection, Simulation=None):

	"""

	:rtype : object
	"""

	isChange = False

	if np.size(Scenario.Iabs) == 1:
		names = ["Top","Bottom", "Left", "Right"]
		boundaries = [Boundary(name, BC=BC.AirLayer, size=0) for name in names]
		Boundaries = copy.deepcopy(boundaries)
		Scenario.createBoundaries(boundaries)
		isChange = True

	if Simulation is not None:
		Simulation.reLoad(Materials, Scenario,Transducer)

	return Scenario, Boundaries, isChange


def labels(Scenario, Materials):
	numLabels    = np.size(np.unique(Scenario.I))
	numMaterials = len(Materials)
	if numLabels == numMaterials:
		return 0
	elif numLabels > numMaterials:
		return 1
	elif numLabels < numMaterials:
		return 2

def isLabelsEquals(Scenario, Materials):
	labels = np.unique(Scenario.I).tolist()
	mat    = [material.Label for material in Materials]
	s1 = set(labels)
	s2 = set(mat)
	if s1.issubset(s2):
		return 0
	else:
		return 1


def materials(Materials):
	mat    = [material.Label for material in Materials]
	length = len(mat)
	unique_Length = np.size(np.unique(mat))
	if length == unique_Length:
		return 0
	else:
		return 1


			
	
	
	
			
			