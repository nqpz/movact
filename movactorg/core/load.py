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
                                 ## Loader ##
                                 ############

#############
## IMPORTS ##
#############
## Global
import sys

## Local
from movactorg.core.parse import *
from movactorg.core.err import *

######################
## CLASS DEFINITION ##
######################
class Loader:
	"""Does different actions based on different arguments"""
	# SETTINGS:
	#### frontend=<frontend>: use <frontend> for running the game
	#### args=<arguments>: do actions based on a list of <arguments>
	#### always_run=True: run an empty game if no arguments are specified
	####                  instead of stopping completely. Useful for GUIs
	
	def __init__(self, **args):
		if 'frontend' in args:
			self.frontend = args['frontend']
		else:
			err('No frontend specified!\n')
		if 'args' in args:
			self.args = args['args']
		else:
			self.args = []
		if 'always_run' in args:
			self.always_run = args['always_run']
		else:
			self.always_run = False
		
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
		   or (arglen == 0 and not self.always_run):
			print """\
Usage: movact FILE|-(h|-help|v|-version) [OPTION]...
Reads and runs hypertext fiction files from the movact format

Options:
  -u, --unpickle    Unpickle FILE instead of parsing it
  -l, --noautoload  Do not attempt to load autosaved game data
  -s, --noautosave  Do not automatically save as you progress
  -d, --debug       Show half-parsed file to check for errors
  -p, --pickle      Pickle FILE into FILE.pickled
  -e, --exit        Quit movact before it even starts; this is useful if you
                    only want to pickle data and not actually run it

  -h, --help        Show this help and exit
  -v, --version     Show version information and exit

Pickling and unpickling are Python-specific ways of storing and reading data in
a clever way. Note that it is not necessary to specify the '-u' flag if FILE has
the extension '.pickled', as movact in such cases will attempt to unpickle the
data automatically.

Autosaving and -loading are based on the titles of stories and not on filenames.\
"""
			try:
				print self.frontend.HELPTEXT
			except:
				pass
		
			sys.exit()
		elif arglen == 1 and (
		   (arg[0][:1] == '-' and arg[0][1:2] != '-' and arg[0].find('v') != -1)
		   or arg[0] == '--version'):
			try:
				print self.frontend.VERSIONTEXT
			except:
				print """\
movact 0.5
Copyright (C) 2009  Niels Serup
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
"""
			sys.exit()
		
		
		self.UNPICKLE = False
		self.AUTOLOAD = True
		self.AUTOSAVE = True
		self.DEBUG    = False
		self.PICKLE   = False
		self.EXIT     = False
		self.FILENAME = None
		
		for x in self.args[1:]:
			if x[:2] == '--':
				option = x[2:]
				if   option == 'unpickle':
					self.UNPICKLE = True
				elif option == 'noautoload':
					self.AUTOLOAD = False
				elif option == 'noautosave':
					self.AUTOSAVE = False
				elif option == 'debug':
					self.DEBUG    = True
				elif option == 'pickle':
					self.PICKLE   = True
				elif option == 'exit':
					self.EXIT     = True
			elif x[:1] == '-':
				options = x[1:]
				for y in options:
					if   y == 'u':
						self.UNPICKLE = True
					elif y == 'l':
						self.AUTOLOAD = False
					elif y == 's':
						self.AUTOSAVE = False
					elif y == 'd':
						self.DEBUG    = True
					elif y == 'p':
						self.PICKLE   = True
					elif y == 'e':
						self.EXIT     = True
		
		if len(self.args) >= 1:
			self.FILENAME = self.args[0]
	
	def do_extra_check(self):
		"""Checks one extra time"""
		if self.FILENAME:
			p_string = '.pickled'
			if self.FILENAME[-len(p_string):] == p_string:
				if self.FILENAME[0] == '\\':
					self.FILENAME = self.FILENAME[1:]
				else:
					self.UNPICKLE = True
	
	def do_actions(self):
		"""Acts"""
		if self.FILENAME:
			story = Parser(file    = self.FILENAME,
			               pickled = self.UNPICKLE,
			               debug   = self.DEBUG   )
			if self.DEBUG:
				return
			
			if self.PICKLE:
				f = open(self.FILENAME + '.pickled', 'w')
				f.write(story.pickle_game_data())
				f.close()
		
		if self.EXIT:
			return
		
		if self.FILENAME:	
			game = self.frontend.Runner(data     = story.get_game_data(),
			                            autoload = self.AUTOLOAD        ,
			                            autosave = self.AUTOSAVE        )
		else:
			game = self.frontend.Runner(data     = [{}, {}]             ,
			                            autoload = self.AUTOLOAD        ,
			                            autosave = self.AUTOSAVE        )
	
