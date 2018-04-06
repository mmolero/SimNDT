#!/usr/bin/env python
# encoding: utf-8
"""
boundary.py

Created by Miguel Molero on 2013-09-14.
Copyright (c) 2013 MMolero. All rights reserved.
"""

from SimNDT.core.constants import *

class Boundary:
    def __init__(self,	name="Top", BC=BC.AirLayer, size=0):
    	self.Name	= name
    	self.BC		= BC
    	self.Size	= size
