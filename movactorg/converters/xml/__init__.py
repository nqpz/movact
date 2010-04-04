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

                            ###################
                            ## XML converter ##
                            ###################

#############
## IMPORTS ##
#############
## Global
from os.path import exists

## Local
from movactorg.converters.convert import *

def tr(txt):
	return txt.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')

######################
## CLASS DEFINITION ##
######################
class Converter(GenericConverter):
	def __init__(self, **args):
		GenericConverter.__init__(self, **args)
		
		if not self.file:
			self.file = 'story.xml'
		else:
			self.file += '.xml'
		
		# Check if the user has defined any templates
		if len(self.files) > 0:
			print 'No templates can be used with this converter.'
			del self.files
		
		# Start the converting process
		self.convert()
	
	def convert(self):
		xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'
		xml += '<story>\n'
		xml += '\t<meta>\n'
		for x in self.meta.items():
			x0m = tr(x[0]).replace(' ', '_')
			xml += '\t\t<'+x0m+'>' + tr(str(x[1])) + '</'+x0m+'>\n'
		xml += '\t</meta>\n'
		
		xml += '\t<main>\n'
		for x in self.main.items():
			header = x[0]
			content = x[1]
			xml += '\t\t<part>\n'
			xml += '\t\t\t<name>' + tr(header) + '</name>\n'
			if len(content) == 2 and content[1][1] == '':
				xml += '\t\t\t<content />\n'
			else:
				xml += '\t\t\t<content>\n'
				for y in content[1:]:
					if y[0]:
						xml += '\t\t\t\t<line>' + tr(y[1]) + '</line>\n'
					else:
						xml += '\t\t\t\t<pointer>\n'
						xml += '\t\t\t\t\t<part>' + tr(y[1]) + '</part>\n'
						xml += '\t\t\t\t\t<text>' + tr(y[2]) + '</text>\n'
						xml += '\t\t\t\t</pointer>\n'
				xml += '\t\t\t</content>\n'
			xml += '\t\t</part>\n'
		xml += '\t</main>\n'
		xml += '</story>\n'
		
		fname = self.file
		while exists(fname):
			fname = '_' + fname
		f = open(fname, 'w')
		f.write(xml)
		f.close()
		
		print 'XML data saved in "'+fname+'".'
