#!/usr/bin/env python
# encoding: utf-8
"""
receivers.py

Created by Miguel Molero on 2013-10-07.
Copyright (c) 2013 MMolero. All rights reserved.
"""

class Receivers:
	
	def __init__(self, method = "Trasmission"):
		self.method = method
		self.receiver_signals = 0


	def setReceivers(self, engine):
		self.receiver_signals = engine.getReceivers()
		
	def getReceivers(self):
		return self.receiver_signals
