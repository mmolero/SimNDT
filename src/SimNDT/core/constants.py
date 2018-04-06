__author__ = 'Miguel Molero'


class BC(object):
	AbsorbingLayer = 0
	AirLayer = 1
	keys = ["Absorbing", "Air"]

class WaveSource(object):
	Longitudinal = 0
	Shear = 1
	LongitudinalAndShear = 2
	keys = ['Longitudinal', 'Shear', 'LongitudinalAndShear']


class TypeSource(object):

	Pressure = 0
	Displacement = 1
	PressureAndDisplacement = 2
	keys = ["Pressure", "Displacement", "PressureAndDisplacement"]


class SignalType(object):
	RaisedCosinePulse = 0
	GaussianSinePulse = 1



