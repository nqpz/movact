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

                                 ############
                                 ## Errors ##
                                 ############

#############
## IMPORTS ##
#############
## Global
import sys

###############
## FUNCTIONS ##
###############
def err(msg = 'Error', exit = True):
	sys.stderr.write(msg + '\n')
	if exit:
		sys.exit(1)

def data_err(data):
	if not data:
		error = 'No data specified.'
	else:
		error = 'Something wrong with the following data:\n' + str(data)
	err(error)

def file_err(filename):
	error = 'Something wrong with file "' + filename + '". Does it even exist?'
	err(error)

def version_err(version):
	error = 'This parser does not understand version "' + version + '". Does it even exist? Try using version "ZERO" instead.'
	err(error)

def syntax_err(text, header, part, line = -1):
	error = 'Syntax error in ' + part + '.' + header + ' on line ' + str(line) + ':\n' + text
	err(error)

def reference_err(refname, header, part, line = -1):
	error = 'Reference error in ' + part + '.' + header + ' on line ' + str(line) + ':\nPart "' + refname + '" does not exist.'
	err(error)

def subpart_err(header, part, line = -1, orig_line = -1):
	error = 'Error: Subpart ' + part + '.' + header + ' on line ' + str(line) + ' already exists on line ' + str(orig_line) + '.'
	err(error)

def non_reference_err(header, part, line = -1):
	error = 'Error: ' + part + '.' + header + ' on line ' + str(line) + ' is not referenced by any part.'
	err(error)

def unknown_err(**info):
	error = ''
	for x in info.items():
		error += str(x[0]) + ':' + str(x[1]) + '; '
	if not error:
		error = 'Error.'
	else:
		error = 'Error. Info: ' + error[:-2]
	err(error)

def python_err(*info):
	error = 'Python error: ' + str(info)
	err(error)

def python_warn(*info):
	error = 'Python error: ' + str(info)
	err(error, False)
