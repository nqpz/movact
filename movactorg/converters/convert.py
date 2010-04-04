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
                          ## Convert runner ##
                          ####################

#############
## IMPORTS ##
#############
## Local
from movactorg.core.defaults import *
from movactorg.core.err import *

######################
## CLASS DEFINITION ##
######################
class GenericConverter:
	"""Runs movact converters"""
	# SETTINGS:
	#### data=<data>: take data from <data>
	#### files=[files]: use [files] as template files
	#### file=<file>: decide output target from this filename
	def __init__(self, **args):
		try:
			self.meta = args['data'][0]
			self.main = args['data'][1]
		except:
			if 'data' in args:
				data_err(args['data'])
			else:
				data_err('')
		
		if not self.main:
			err('No main part.')
		
		if 'files' in args:
			self.files = args['files']
		else:
			self.files = []
		
		if 'file' in args:
			self.file = args['file']
		else:
			self.file = None
		
		# Insert default meta values in places that do not have values
		self.meta = base_on(self.meta)
	
	def get_file_contents(self, num = 0):
		"""Tries to read from file no. <num>, then <num>+1, etc."""
		# Will return the text of the first valid file after <num>, or None if
		# no valid files exist.
		try:
			f = open(self.files[num], 'r')
			c = f.read()
			f.close()
		except:
			c = None
		
		del self.files[num] # Length goes down by 1
		if len(self.files) > 0:
			return self.get_file_contents()
		else:
			return None
