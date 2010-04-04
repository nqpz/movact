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

                            ####################
                            ## HTML converter ##
                            ####################

#############
## IMPORTS ##
#############
## Global
from os.path import realpath, dirname, exists
from os import mkdir
from re import sub
from urllib import quote

## Local
from movactorg.converters.convert import *

def secure(txt):
	"""Makes sure links stay sane"""
	return quote(txt).replace('%', '.')

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
		
		# Check if the user has defined any templates
		if len(self.files) > 0:
			self.html_template = self.get_file_contents()
			if len(self.files) > 0:
				self.css_template = self.get_file_contents()
				if len(self.files) > 0:
					print\
'Only 2 templates can be used with this converter: HTML and CSS.'
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
		
		# Start the converting process
		self.convert()
	
	def convert(self):
		self.makedir()
		self.produce_index_file()
		self.save_css_styles()
		self.loop()
		print 'HTML files generated in "'+self.dir+'".'
	
	def makedir(self):
		self.dir = self.file
		while exists(self.dir):
			self.dir = '_' + self.dir
		self.dir += '/'
		mkdir(self.dir)
	
	def produce_index_file(self):
		text = '<p>' + self.meta['start'] + '</p>\n\
<p><a href=\'pstart.html\'>' + self.meta['title'] + '</a></p>\n'
		
		html = self.html_template
		html = html.replace('<!--movact content-->', text)
		html = html.replace('<!--movact title-->', self.meta['title'])
		
		f = open(self.dir+'index.html', 'w')
		f.write(html)
		f.close()
	
	def save_css_styles(self):
		f = open(self.dir+'style.css', 'w')
		f.write(self.css_template)
		f.close()
	
	def loop(self):
		"""Loops through main items and saves contents to files"""
		for parts in self.main.items():
			header = parts[0]
			part = parts[1]
			text = ''
			refsnum = 0
			for x in part[1:]:
				# Print contents and register any pointer lines
				if x[0]:
					if not x[1]:
						text += '<p>&nbsp;</p>\n'
					else:
						text += '<p>' + x[1] + '</p>\n'
				else:
					p = self.meta['points'][refsnum]
					text += '<p><a href=\'p'+secure(x[1])+'.html\'>' +\
					        p[0] + x[2] + '</a></p>\n'
					refsnum += 1
				
				if not part[0]:
					text += '<hr />\n' + self.meta['end']
			
			html = self.html_template
			html = sub('(\\n?)\s*<!--movact content-->', '\\1'+text, html)
			html = sub('(\\n?)\s*<!--movact title-->', '\\1'+\
			                                           self.meta['title'] +\
			                                           ' ["'+header+'"]', html)
			
			f = open(self.dir+'p'+secure(header)+'.html', 'w')
			f.write(html)
			f.close()
