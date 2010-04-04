#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   movact: A program that reads, runs and converts hypertext fiction files
#   Copyright (C) 2009  Niels Serup

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

                                 ############
                                 ## Runner ##
                                 ############

#############
## IMPORTS ##
#############
## Global
from os.path import expanduser, isdir
from os import makedirs
try: import cPickle as pickle
except: import pickle

## Local
from movactorg.core.err import *
from movactorg.core.parse import *
from movactorg.core.defaults import *


###############
## FUNCTIONS ##
###############
def char_ok(c):
	"""Checks if a character is within certain ASCII ranges"""
	try:
		o = ord(c)
		# Only allow letters and numbers
		return (o >= 48 and o <= 57) or (o >= 65 and o <= 90) or (o >= 97 and o <= 122)
	except:
		return False

def generate_special_string(t, l = 6):
	"""Generates a fairly unique string based on another string"""
	if t == '':
		return '0' * l
	
	n = ''
	for x in t:
		if char_ok(x):
			n += x
	
	nl = len(n)
	if nl == l:
		return n
	
	d = float(nl) / float(l)
	nn = ''
	for i in range(l):
		nn += n[int(d*i)]

	return nn

######################
## CLASS DEFINITION ##
######################
class GenericRunner:
	"""Runs movact games"""
	# SETTINGS:
	#### data=<data>: take data from <data>
	#### autoload=False: do not attempt to automatically load autosaved data
	#### autosave=False: do not automatically save as you progress
	
	def __init__(self, **args):
		try:
			self.meta = args['data'][0]
			self.main = args['data'][1]
		except:
			if 'data' in args:
				data_err(args['data'])
			else:
				data_err('')
		
		self.ok = True
		if not self.main: # self.meta is not crucial, as it can rely on default
		                  # values
			self.ok = False
		
		self.AUTOLOAD = True
		self.AUTOSAVE = True
		if 'autoload' in args and not args['autoload']:
			self.AUTOLOAD = False
		if 'autosave' in args and not args['autosave']:
			self.AUTOSAVE = False
		
		# Insert default meta values in places that do not have values
		self.meta = base_on(self.meta)
		
		if self.ok:
			# Only really start it if there's data
			self.part_name = 'start'
			self.visited_parts = []
			
			autosave_dir = expanduser('~') + '/.movact/autosaves/'
			if not isdir(autosave_dir):
				makedirs(autosave_dir)
				
			self.autosave_filename = autosave_dir + generate_special_string(self.meta['title'])
			if self.AUTOLOAD:
				self.load(self.autosave_filename, False)
	
	def load(self, filename, err = True):
		"""Loads a file containing game data"""
		try:
			f = open(filename, 'r')
			v = pickle.load(f)
			f.close()
			t = v[-1]
			if t in self.main:
				v.pop()
				self.visited_parts = v
				self.part_name = t
				return True
			else:
				return False
		except Exception, erred:
			if err:
				python_warn(erred)
			return False
	
	def save(self, filename, mention = True):
		"""Saves current state to a file"""
		try:
			f = open(filename, 'w')
			pickle.dump(self.visited_parts, f)
			f.close()
			return True
		except Exception, erred:
			if mention:
				python_warn(erred)
			return False
	
	def autosave(self):
		"""Automatically saves status"""
		if self.AUTOSAVE:
			self.save(self.autosave_filename, False)
	
	def open(self, filename, autounpickle = True):
		try:
			unpickle = False
			p_string = '.pickled'
			if filename[-len(p_string):] == p_string and autounpickle:
				if filename[0] == '\\':
					filename = filename[1:]
				else:
					unpickle = True
			
			story = Parser(file    = filename,
						   pickled = unpickle)
			data = story.get_game_data()
			
			GenericRunner.__init__(self,
								   data     = data         ,
								   autoload = self.AUTOLOAD,
								   autosave = self.AUTOSAVE)
			return True
		except:
			return False
