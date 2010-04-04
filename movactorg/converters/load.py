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
                            ## Convert loader ##
                            ####################

#############
## IMPORTS ##
#############
## Global
import sys
from os.path import dirname

## Local
from movactorg.core.parse import *

######################
## CLASS DEFINITION ##
######################
class Loader:
	"""Does different actions based on different arguments"""
	# SETTINGS:
	#### args=<arguments>: do actions based on a list of <arguments	
	def __init__(self, **args):
		if 'args' in args:
			self.args = args['args']
		else:
			self.args = []
		
		self.parse_arguments()
		self.do_extra_check()
		self.do_actions()
	
	def parse_arguments(self):
		"""Parses the arguments"""
		arg = self.args
		arglen = len(arg)
		if (arglen == 1 and (
		   (arg[0][:1] == '-' and arg[0][1:2] != '-' and arg[0].find('h') != -1)
		                or arg[0] == '--help'))\
		   or arglen == 0:
			print """\
Usage: movact-convert FILE...|-(h|-help|v|-version) [FORMAT]
Converts hypertext fiction files from the movact format to other formats

Options:
  -h, --help       Show this help and exit
  -v, --version    Show version information and exit

Formats:
  html            Converts a movact file to a bunch of XHTML pages
  javascript      Converts a movact file to one XHTML page where JavaScript
        (default) is used to navigate
  xml             Converts a movact file to a logically structured XML file
  text            Converts a movact file to a simple, well-organized text file

If you specify more than one file, movact-convert will attempt to read the
second file as a template file. For example, you could type:

    $ movact-convert a_story.mvct some_template.html tmpl.css

movact-convert would then read "some_template.html" and replace
'<!--movact content-->' with the actual output, and
'<!--movact title-->'   with the title of the story.
It would also create a file named 'style.css' with the contents of 'tmpl.css'\
"""
		
			sys.exit()
		elif arglen == 1 and (
		   (arg[0][:1] == '-' and arg[0][1:2] != '-' and arg[0].find('v') != -1)
		   or arg[0] == '--version'):
			print """\
movact-convert 0.5.1
Copyright (C) 2009, 2010  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
"""
			sys.exit()
		
		self.FILENAMES = self.args
		self.FORMAT = 'javascript'
		larg = self.args[-1].lower()
		if len(self.args) > 1 and\
		larg in ('html', 'javascript', 'xml', 'text'):
			self.FORMAT = larg
			self.FILENAMES = self.args[:-1]
		
		self.UNPICKLE = False
	
	def do_extra_check(self):
		"""Checks one extra time"""
		p_string = '.pickled'
		if self.FILENAMES[0][-len(p_string):] == p_string:
			if self.FILENAMES[0][0] == '\\':
				self.FILENAMES[0] = self.FILENAMES[0][1:]
			else:
				self.UNPICKLE = True
	
	def do_actions(self):
		"""Acts"""
		story = Parser(file    = self.FILENAMES[0],
		               pickled = self.UNPICKLE    )
		
		if self.FORMAT == 'html':
			import movactorg.converters.html as converter
		elif self.FORMAT == 'javascript':
			import movactorg.converters.javascript as converter
		elif self.FORMAT == 'xml':
			import movactorg.converters.xml as converter
		elif self.FORMAT == 'text':
			import movactorg.converters.text as converter
		
		fname = self.FILENAMES[0]
		fname = fname[len(dirname(fname))+1:]
		
		converter.Converter(data   = story.get_game_data(),
		                    files  = self.FILENAMES[1:]   ,
		                    file   = fname                )
	
