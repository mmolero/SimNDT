#!/usr/bin/env python
# encoding: utf-8
"""
geometryObjects.py

Created by Miguel Molero on 2013-09-04.
Copyright (c) 2013 MMolero. All rights reserved.
"""


class Ellipse:
	
	def __init__(self,x0=50,y0=50,a=10,b=5,theta=0,Label=0):
		self.x0 = x0
		self.y0 = y0
		self.a  = a
		self.b  = b
		self.theta = theta
		self.Label = Label
		self.Name = "ellipse"

		
class Circle:
	
	def __init__(self,x0=50,y0=50, r=10,Label=0):
		self.x0 = x0
		self.y0 = y0
		self.r  = r
		self.Label = Label
		self.Name = "circle"
	

class Rectangle:
	def __init__(self,x0=50,y0=50, W=50,H=50,theta=0,Label=0):
		self.x0 = x0
		self.y0 = y0
		self.W  = W
		self.H  = H
		self.theta = theta
		self.Label = Label
		self.Name = "rectangle"
		
class Square:
	def __init__(self,x0=50,y0=50, L=50,theta=0,Label=0):
		self.x0 = x0
		self.y0 = y0
		self.L  = L
		self.theta = theta
		self.Label = Label
		self.Name = "square"
	
	
class Inclusions:
	def __init__(self, Diameter=1.0, Fraction=0.10, Label=60):
		self.Diameter = Diameter
		self.Fraction = Fraction
		self.Label    = Label
		self.Name     = "inclusion"




class Concrete2Phase:
	def __init__(self, Fraction=0.1, LabelAggregate=40, MinDiameter=0.5, MaxDiameter=10.0,
				 Grading=0.10, MinAspectRatio=0.5, MaxAspectRatio=0.80):

		self.Fraction = Fraction
		self.LabelAggregate = LabelAggregate
		self.MinDiameter = MinDiameter
		self.MaxDiameter = MaxDiameter
		self.Grading = Grading
		self.MinAspectRatio = MinAspectRatio
		self.MaxAspectRatio = MaxAspectRatio
		self.Name = "Concrete2Phase"


class Concrete2PhaseImmersion:
	def __init__(self, Fraction=0.1, LabelMatrix=40, MinDiameter=0.5, MaxDiameter=10.0,
				 Grading=0.10, MinAspectRatio=0.5, MaxAspectRatio=0.80,
				 BoxWidth=50, BoxHeight=50, isCircular=False, LabelAggregate=80):

		self.Fraction = Fraction
		self.LabelMatrix = LabelMatrix
		self.MinDiameter = MinDiameter
		self.MaxDiameter = MaxDiameter
		self.Grading = Grading
		self.MinAspectRatio = MinAspectRatio
		self.MaxAspectRatio = MaxAspectRatio

		self.BoxWidth = BoxWidth
		self.BoxHeight = BoxHeight
		self.isCircular = isCircular
		self.LabelAggregate = LabelAggregate

		self.Name = "Concrete2PhaseImmersion"

		
		
class Concrete3Phase:
	def __init__(self, Fraction=10, LabelAggregate=40, MinDiameter=0.5, MaxDiameter=10.0,
				 Grading=0.10, MinAspectRatio=0.5, MaxAspectRatio=0.80,
				  FractionsAir = 0.01, LabelAir =80, MinDiameterAir=0.5, MaxDiameterAir=1.0, GradingAir=0.1):

		self.Fraction = Fraction
		self.LabelAggregate = LabelAggregate
		self.MinDiameter = MinDiameter
		self.MaxDiameter = MaxDiameter
		self.Grading = Grading
		self.MinAspectRatio = MinAspectRatio
		self.MaxAspectRatio = MaxAspectRatio

		self.FractionAir = FractionsAir
		self.LabelAir = LabelAir
		self.MinDiameterAir = MinDiameterAir
		self.MaxDiameterAir = MaxDiameterAir
		self.GradingAir = GradingAir


		self.Name = "Concrete3Phase"

class Concrete3PhaseImmersion:

	def __init__(self, LabelMatrix = 40,  Fraction=0.1, LabelAggregate=80, MinDiameter=0.5, MaxDiameter=10.0,
				 Grading=0.10, MinAspectRatio=0.5, MaxAspectRatio=0.80,
				  FractionsAir = 0.01, LabelAir =120, MinDiameterAir=0.5, MaxDiameterAir=1.0, GradingAir=0.1,
				  BoxWidth=50, BoxHeight=50, isCircular=False ):

		self.Fraction = Fraction
		self.LabelMatrix = LabelMatrix
		self.LabelAggregate = LabelAggregate
		self.MinDiameter = MinDiameter
		self.MaxDiameter = MaxDiameter
		self.Grading = Grading
		self.MinAspectRatio = MinAspectRatio
		self.MaxAspectRatio = MaxAspectRatio

		self.FractionAir = FractionsAir
		self.LabelAir = LabelAir
		self.MinDiameterAir = MinDiameterAir
		self.MaxDiameterAir = MaxDiameterAir
		self.GradingAir = GradingAir

		self.BoxWidth = BoxWidth
		self.BoxHeight = BoxHeight
		self.isCircular = isCircular




		self.Name = "Concrete3PhaseImmersion"