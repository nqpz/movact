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

                             ##############
                             ## Defaults ##
                             ##############

default = {}

default['points'] = (
	('1. ', ('1')),
	('2. ', ('2')),
	('3. ', ('3')),
	('4. ', ('4')),
	('5. ', ('5')),
	('6. ', ('6')),
	('7. ', ('7')),
	('8. ', ('8')),
	('9. ', ('9'))
)
default['title'] = 'A story'
default['start'] = 'Welcome to a story.'
default['end'] = 'Farewell.'
default['prompt'] = 'Go to: '
default['again'] = 'Try again.'
default['error'] = 'Error.'
default['separator'] = '**********'
default['load'] = 'Choose file: '
default['load-gui'] = 'Choose file'
default['save'] = 'Choose file: '
default['save-gui'] = 'Choose file'
default['open'] = 'Choose file: '
default['open-gui'] = 'Choose file'
default['loaded'] = 'Savefile loaded.'
default['load error'] = 'Contents are not savedata.'
default['saved'] = 'Savedata saved to file.'
default['opened'] = 'movact file opened.'
default['confirm'] = 'Are you sure? (y/N) '
default['confirm-gui'] = 'Are you sure?'
default['confirmed'] = ('y', 'yes') # Case-ignorant
default['quit command'] = '/quit'
default['load command'] = '/load'
default['save command'] = '/save'
default['back command'] = '/back'
default['reset command'] = '/reset'
default['open command'] = '/open'
default['current command'] = '/current'
default['open button'] = 'Open'
default['back button'] = 'Back'
default['reset button'] = 'Reset'
default['load button'] = 'Load'
default['save button'] = 'Save'
default['quit button'] = 'Quit'

default['start-gui'] = default['start']
default['end-gui'] = default['end']
default['version'] = 'ZERO'

def base_on(meta):
	"""Adds default values to meta dict where no values appear"""
	global default
	
	for x in default.items():
		if not x[0] in meta and not x[0] in ('start-gui', 'end-gui'):
			meta[x[0]] = x[1]
	
	if not 'start-gui' in meta:
		meta['start-gui'] = meta['start']
	if not 'end-gui' in meta:
		meta['end-gui'] = meta['end']
	
	return meta

