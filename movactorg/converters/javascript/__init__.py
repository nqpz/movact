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

                       ##########################
                       ## JavaScript converter ##
                       ##########################

#############
## IMPORTS ##
#############
## Global
from os.path import realpath, dirname, exists
from re import sub

## Local
from movactorg.converters.convert import *

try:
	from json import dumps as _toJSON # Available in Python 2.6
except:
	import movactorg.external.simplejson_encoder as simplejson
	JSONEncoder = simplejson.JSONEncoder()
	def _toJSON(obj):
		global JSONEncoder
		return JSONEncoder.encode(obj)

def toJSON(obj):
	return _toJSON(obj).replace('\\n', '\\\\n')

######################
## CLASS DEFINITION ##
######################
class Converter(GenericConverter):
	def __init__(self, **args):
		GenericConverter.__init__(self, **args)
		
		if not self.file:
			self.file = 'story.html'
		else:
			self.file += '.html'
		
		self.path = dirname(realpath(__file__)) + '/'
		
		self.html_template = None
		self.css_template = None
		self.js_template = None
		
		# Check if the user has defined any templates
		if len(self.files) > 0:
			self.html_template = self.get_file_contents()
			if len(self.files) > 0:
				self.css_template = self.get_file_contents()
				if len(self.files) > 0:
					self.js_template = self.get_file_contents()
					if len(self.files) > 0:
						print\
'Only 3 templates can be used with this converter; HTML, CSS and JavaScript.'
			del self.files
		
		# Eventually pick default templates
		if not self.html_template:
			f = open(self.path + 'template.html', 'r')
			self.html_template = f.read()
			f.close()
		if not self.css_template:
			f = open(self.path + 'style.css', 'r')
			self.css_template = f.read()
			f.close()
		if not self.js_template:
			f = open(self.path + 'script.js', 'r')
			self.js_template = f.read()
			f.close()
		
		# Start the converting process
		self.convert()
	
	def convert(self):
		"""Actually converts the movact data"""
		
		code = self.js_template % (toJSON(self.meta), toJSON(self.main))
		
		html = self.html_template
		html = sub('(\\n?)\s*<!--movact title-->', '\\1'+self.meta['title'], html)
		html = sub('(\\n?)\s*<!--movact style-->', '\\1'+self.css_template, html)
		html = sub('(\\n?)\s*/\*movact code\*/', '\\1'+code, html)
		html = sub('(\\n?)\s*<!--movact start-->', '\\1'+self.meta['start'], html)
		
		fname = self.file
		while exists(fname):
			fname = '_' + fname
		f = open(fname, 'w')
		f.write(html)
		f.close()
		
		print 'HTML/JavaScript data saved in "'+fname+'".'
