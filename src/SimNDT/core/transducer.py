#!/usr/bin/env python
# encoding: utf-8
"""
transducer.py

Created by Miguel Molero on 2013-09-25.
Copyright (c) 2013 MMolero. All rights reserved.
"""



class Transducer:

	def __init__(self, name         = 'emisor',
	                   Size         = 10, CenterOffset = 0, BorderOffset = 0, Location     = "Top",
					   PointSource  = False,  EnableWindow = False, Field=False, PZT=False):

		self.Name         = name
		self.Size		  = Size
		self.CenterOffset = CenterOffset
		self.BorderOffset = BorderOffset
		self.SizePixel	  = 0
		self.Location	  = Location
		self.PointSource  = PointSource
		self.Window       = EnableWindow
		self.Field        = Field
		self.PZT          = PZT
		
	
	def __str__(self):
		return "Transducer: " 

	def __repr__(self):
		return "Transducer: "
