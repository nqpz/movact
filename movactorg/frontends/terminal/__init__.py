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

                            #######################
                            ## Terminal frontend ##
                            #######################
#############
## IMPORTS ##
#############
## Global
import sys
try: import readline
except: pass

## Local
from movactorg.core.run import *

##########################################################
HELPTEXT = '\nThis is the terminal (console) frontend.' ##
##########################################################

###############
## FUNCTIONS ##
###############
def fancy_print(t, m = 80):
	"""Fancifies text and prints it"""
	t  = ((m - len(t))/2 - 1) * '#' + ' ' + t + ' '
	t += (m - len(t)) * '#'
	print t

def shorten_long_lines(atxt, w = 80):
	"""Makes sure that lines exceeding <w> characters are shortened and \
continued on subsequent lines"""
	
	if w < 2 or len(atxt) < 2:
		return atxt
	
	stxt = atxt.split('\n')
	ntxt = ''
	for txt in stxt:
		while txt:
			if len(txt) <= w:
				ntxt += txt
				break
			if txt[:w].find(' ') == -1:
				ntxt += txt[:w - 1] + '-\n'
				txt = txt[w - 1:]
				continue
			cw = w
			while txt[cw] != ' ':
				cw -= 1
			ntxt += txt[:cw] + '\n'
			txt = txt[cw + 1:]
		ntxt += '\n'

	ntxt = ntxt[:-1] # Remove last appended extra newline
	return ntxt

def get_input(prompt = ''):
	"""Makes sure that getting input works well with readline"""
	# Save current settings
	saved = sys.stdout
	
	# Temporarily reset standard out while receiving input
	sys.stdout=sys.__stdout__
	result = raw_input(prompt)
	
	# Change back
	sys.stdout = saved
	
	return result

######################
## CLASS DEFINITION ##
######################
class ModifiedOutputWriting:
	"""Thinks, then writes"""
	def write(self, txt):
		sys.__stdout__.write(shorten_long_lines(txt))

class Runner(GenericRunner):
	def __init__(self, **args):
		
		# Overwrite standard out for more extensive printing possibilites
		set_output = ModifiedOutputWriting()
		sys.stdout = set_output
		
		# General stuff
		GenericRunner.__init__(self, **args)
		
		self.story_done = False
		self.rerun = True
		while self.rerun:
			self.rerun = False
			self.run()
	
	def run(self):
		"""Runs a movact game"""
		
		if self.meta['start']:
			print self.meta['start']
			print self.meta['separator']
		
		done = False
		while not done:
			# Find and print contents
			part = self.main[self.part_name]
			refs = []
			text = ''
			for x in part[1:]:
				# Print contents and register any pointer lines
				if x[0]:
					text += x[1] + '\n'
				else:
					p = self.meta['points'][len(refs)]
					text += p[0] + x[2] + '\n'
					refs.append((p[1], x[1]))
			text = text[:-1]
			print text
			
			
			self.story_done = False # Story is by default not over..
			if not part[0]:
				# ... Though now it is.
				print self.meta['separator']
				print self.meta['end']
				self.story_done = True
			self.visited_parts.append(self.part_name)
			
			self.autosave()
			
			# Get input
			input_ok = False
			while not input_ok:
				print_again = True # Print error message on wrong input
				inp = get_input(self.meta['prompt']).rstrip()
				if not inp:
					continue
				for x in refs:
					if inp in x[0]:
						self.part_name = x[1]
						input_ok = True
						print self.meta['separator']
						break
				
				if not input_ok:
					if inp == self.meta['quit command']:
						if self.confirmed():
							input_ok = True
							done = True
							break
						else:
							print_again = False
							print self.meta['separator']
							print text
					elif inp == self.meta['load command']:
						if self.confirmed():
							self.prepare_load()
							input_ok = True
							print self.meta['separator']
							break
						else:
							print_again = False
							print self.meta['separator']
							print text
					elif inp == self.meta['save command']:
						self.prepare_save()
						print_again = False
						print self.meta['separator']
						print text
					elif inp == self.meta['back command']:
						if len(self.visited_parts) > 1:
							self.visited_parts.pop()
							self.part_name = self.visited_parts[-1]
							self.visited_parts.pop()
							input_ok = True
							print self.meta['separator']
						else:
							print_again = False
							print self.meta['error']
							print self.meta['separator']
							print text
					elif inp == self.meta['open command']:
						if self.confirmed():
							if not self.prepare_open():
								print_again = False
								print self.meta['error']
								print self.meta['separator']
								print text
							else:
								done = True
								self.rerun = True
								input_ok = True
								break
						else:
							print_again = False
							print self.meta['separator']
							print text
					elif inp == self.meta['reset command']:
						if self.confirmed():
							self.part_name = self.visited_parts[0]
							self.visited_parts = []
							input_ok = True
							print self.meta['separator']
						else:
							print_again = False
							print self.meta['separator']
							print text
					elif inp == self.meta['current command']:
						fancy_print('"' + self.part_name + '" (' + str(len(self.visited_parts)-1) + ')')
						print_again = False
						print text
						
				if not input_ok and print_again:
					print self.meta['again']
					print self.meta['separator']
					print text
					if self.story_done:
						print self.meta['separator']
						print self.meta['end']
	
	def confirmed(self):
		"""Asks the user if they are sure"""
		if self.story_done:
			return True
		
		inp = get_input(self.meta['confirm']).strip().lower()
		return inp in self.meta['confirmed']
	
	def prepare_load(self):
		"""Prepares to load a file containing savedata"""
		inp = get_input(self.meta['load'])
		self.load(inp)
	
	def load(self, filename, err = True):
		l = GenericRunner.load(self, filename, err)
		if l:
			print self.meta['loaded']
		elif err:
			print self.meta['load error']
	
	def prepare_save(self):
		"""Prepares to save savedata to a file"""
		inp = get_input(self.meta['save'])
		self.save(inp)
	
	def save(self, filename, mention = True):
		s = GenericRunner.save(self, filename, mention)
		if s and mention:
			print self.meta['saved']
	
	def prepare_open(self):
		"""Prepares to open a movact file"""
		inp = get_input(self.meta['open'])
		o = self.open(inp)
		if o:
			print self.meta['opened']
			print self.meta['separator']
		return o
