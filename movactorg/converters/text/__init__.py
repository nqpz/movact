#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   movact: A program that reads, runs and converts hypertext fiction files
#   Copyright (C) 2009, 2010  Niels Serup

#   This file is part of movact.
#
#   movact is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   movact is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with movact.  If not, see <http://www.gnu.org/licenses/>.

#   Maintained by Niels Serup <ns@metanohi.org>

##''''''''''' Documentation and downloads are available at '''''''''''##
################# http://metanohi.org/projects/movact/ #################

                            ####################
                            ## Text converter ##
                            ####################

#############
## IMPORTS ##
#############
## Global
from os.path import exists

## Local
from movactorg.converters.convert import *

######################
## CLASS DEFINITION ##
######################
class Converter(GenericConverter):
	def __init__(self, **args):
		GenericConverter.__init__(self, **args)
		
		if not self.file:
			self.file = 'story.txt'
		else:
			self.file += '.txt'
		
		# Check if the user has defined any templates
		if len(self.files) > 0:
			print 'No templates can be used with this converter.'
			del self.files
		
		# Start the converting process
		self.convert()
	
	def convert(self):
		self.lst = ['start']
		self.look_recursively('start')
		
		text = self.meta['start'] + '\n'
		for i in range(len(self.lst)):
			p = str(i+1)
			lp = len(p)
			t = '-' * (lp+3)
			text += '·'+t+'·\n| '+p+'. |\n·'+t+'·\n'
			# Like:
			# ·----·
			# | 1. |
			# ·----·
			#
			
			x = self.main[self.lst[i]]
			for y in x[1:]:
				if y[0]:
					text += y[1] + '\n'
				else:
					text += '#### ' + y[2] + ' >> ' + self.which(y[1]) + '\n'
			if not x[0]:
				text += '\n' + self.meta['end'] + '\n'
			text += '\n'
			
		fname = self.file
		while exists(fname):
			fname = '_' + fname
		f = open(fname, 'w')
		f.write(text)
		f.close()
		
		print 'Text saved in "'+fname+'".'
	
	def which(self, string):
		for i in range(len(self.lst)):
			if self.lst[i] == string:
				return str(i+1)
	
	def look_recursively(self, partname):
		tmp = []
		for x in self.main[partname][1:]:
			if not x[0] and x[1] not in self.lst:
				self.lst.append(x[1])
				tmp.append(x[1])
		for x in tmp:
			self.look_recursively(x)
