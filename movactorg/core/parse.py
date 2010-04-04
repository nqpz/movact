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
                                 ## Parser ##
                                 ############

#############
## IMPORTS ##
#############
## Global
import re
from os.path import exists
try: import cPickle as pickle
except: import pickle

## Local
from movactorg.core.err import *
from movactorg.core.defaults import *

###############
## FUNCTIONS ##
###############
def is_first(string, line):
	"""Checks if the characters in <string> are first in <line>"""
	return line[:len(string)] == string

def unescape_eot_specials(text):
	"""Unescapes special end of text strings"""
	text = '  '+text
	for y in '---', '[end]':
		ly = len(y)
		if text[-ly:] == y:
			if text[-ly-1] != '\\':
				text = text[:-ly]
			else:
				text = text[:-ly-1] + y
	return text[2:]

######################
## CLASS DEFINITION ##
######################
class Parser:
	"""Parses raw data into movact data"""
	# SETTINGS:
	#### data=<data>: take data from <data>
	#### file=<file>: open <file> and read data
	#### pickled=True: use raw data, do not parse
	#### debug=True: show half-parsed lines (does not work for pickled data)
	####
	#### data takes precedence over file.
	
	def __init__(self, **args):
		if 'data' in args:
			data = str(args['data'])
		elif 'file' in args:
			fname = args['file']
			try:
				f = open(fname, 'U') # Universal newline support,
				### see http://www.python.org/dev/peps/pep-0278/
				data = f.read()
				f.close()
			except Exception, erred:
				if not exists(fname):
					file_err(fname)
				python_err(erred)
			except:
				unknown_err(file=fname)
		else:
			data = ''
		
		if data == '':
			data_err(data)
		
		# Pickled or not?
		self.pickled = False
		if 'pickled' in args:
			if args['pickled']:
				self.pickled = True
		# To be debugged or not?
		self.debug = False
		if 'debug' in args:
			if args['debug']:
				self.debug = True
		
		# Prepare
		self.data = data
		self.meta = {}
		self.main = {}
		
		# Parse
		self.parse()
	
	def parse(self):
		"""Binds together the various parse functions"""
		if self.pickled:
			self.unpickle_game_data()
		else:
			self.escape_blocked_text() # Eg. "%$#abc$%" => "\#abc"
			self.remove_comments() # Both '#...', '//...' and '/*...*/'
			
			if self.debug:
				self.print_lines()
				return
			
			version = self.get_version()
			if version != 'ZERO': # This parser only understands ZERO
				version_err(version)
			
			# Split data into groups
			meta, main, none_lines = self.extract_data()
			
			## Organize meta data
			self.group_meta_data(meta, none_lines) # Will save in self.meta
			self.meta['version'] = version # Add version to meta data
			
			## Organize main data
			self.group_main_data(main, none_lines) # Will save in self.main
			self.look_for_non_referenced_parts() # Will err if some are found
			
			# Delete line numbers and turn lists into tuples
			for x in self.main.keys():
				del self.main[x][0]
				self.main[x] = tuple(self.main[x])
			
			# To avoid data clutter, check if meta items match default meta
			# items, and remove them if they do.
			for x in self.meta.items():
				if x[0] in default: # Allow meta data that isn't actually used.
					if x[1] == default[x[0]]:
						del self.meta[x[0]] # No need to keep it if it's a default value
			
		del self.data # Not needed anymore
	
	def escape_blocked_text(self):
		"""Escapes text inside the '%$' and '$%' strings, \
which are subsequently removed"""
		
		# This function first searches for blocks, in which data is then
		# escaped but NOT replaced. As the escaped data will most likely take up
		# a different amount of space, directly replacing the places in the data
		# would be a mess. Instead the escaped data is temporarily saved in a
		# variable that also holds info on the starting and ending position of
		# the text.
		to_be_changed = []
		
		unescapees = '%$', '$%' # '\%$' => '%$', etc.
		escapees = '//', '#', '/*' # '#abc' => '\#abc', etc. 
		esc_only_if_first = r'\.', r'\[end]', '---' # Must be regex-ok
		
		e = 2 # Extra spaces in front of data (poor hack)
		data = ' '*e + self.data
		leng = len(self.data)
		continue_when = 0
		for i in range(e,leng+e):
			if continue_when > i: continue
			
			if data[i-1:i+1] == '%$' and data[i-2] != '\\':
				end = data.find('$%', i+1) - 1
				while data[end] == '\\':
					f = data.find('$%', end+3) - 1
					if f == -1:
						break
					else:
						end = f
				
				nd = data[i+1:end+1] # The entire block (without '%$' and '$%')
				for x in esc_only_if_first:
					nd = re.sub(r'\n(\s*)' + x, '\\n\\1\\' + x, '\n' + nd)[1:]
				for x in escapees:
					nd = nd.replace(x, '\\' + x)
				
				to_be_changed.append((i-1, end+3, nd))
				
				continue_when = end+3 # Do not continue finding blocks until
				                      # having passed the '$%' of this block
		
		ndata = ''
		offset = 0
		for x in to_be_changed:
			ndata += data[offset:x[0]] + x[2]
			offset = x[1]
		ndata += data[offset:] # The text after the last '$%'
		ndata = ndata[e:]
		
		for x in unescapees:
			ndata = ndata.replace('\\' + x, x)
		
		self.data = ndata
	
	def remove_comments(self):
		"""Removes comments and replaces them with 'none-lines' if no text"""
		
		# '#...', '//...' and '/*...*/' comments are removed.
				
		# To make things easier to grasp (and perhaps slower), removing comments
		# is split into different steps. It's very easy to just remove comments,
		# but when the line numbers of a text are important for the purpose of
		# printing correct errors, it gets a bit more difficult.
		
		#### PART 1 ####
		# This part searches for comments and saves their locations
		pairs = []
		e = 2
		data = ' '*e + self.data
		leng = len(self.data)
		continue_when = 0
		for i in range(e,leng+e):
			if continue_when > i: continue
			
			if data[i-1:i+1] == '/*' and data[i-2] != '\\':
				end = data.find('*/', i) + 1
				pairs.append([i-1-e, end+1-e])
				continue_when = end
			
			elif data[i] == '#' and data[i-1] != '\\':
				nl = data.find('\n', i)
				pairs.append([i-e, nl-e])
				continue_when = nl
			
			elif data[i-1:i+1] == '//' and data[i-2] != '\\':
				nl = data.find('\n', i)
				pairs.append([i-1-e, nl-e])
				continue_when = nl
		
		data = data[e:]
		
		#### PART 2 ####
		# This part changes the text into a list of lines. If a comment spans
		# over more than one line, or if it takes up one whole line, one or more
		# 'none-lines' will be appended to the list of lines. Note that text
		# lines in this part do not necessarily take up one whole line.
		# A line like this may exist.
		#
		#   ABC/*COMMENT*/CBA
		#
		# In this case, the list of lines will be extended with ['ABC', 'CBA'],
		# even though the strings are not on separate lines. So, 'lines' do not
		# mean the same as lines with newlines.
		
		ndata = ['']            # Important that it has a zero value
		pairs.insert(0, [0, 0]) # Important that it has a zero value
		for i in range(1, len(pairs)):
			pn = pairs[i]
			pm = pairs[i-1]
			comment = data[pn[0]:pn[1]]
			
			ndata.append(data[pm[1]:pn[0]]) # Text before the comment
			
			if comment.find('\n') == -1:
				if data[pn[0]-1] == '\n' and data[pn[1]] == '\n':
					# If the comment takes up one whole line
					ndata.append(None)
			else:
				# If the comment spans over several lines
				nls = -1
				for x in comment:
					if x == '\n':
						nls += 1
				if data[pn[0]-1] == '\n': # Before comment
					nls += 1
				if data[pn[1]] == '\n':   # After comment
					nls += 1
				if nls == 0:
					# In this case, the text will look like this:
					#
					#   TEXT/*COMMENT
					#   COMMENT*/TEXT
					#
					# ..which is why a newline must be appended to the text
					# before the comment:
					ndata[len(ndata)-1] += '\n'
				elif nls > 0:
					for j in range(nls):
						ndata.append(None)
		
		ndata.append(data[pairs[len(pairs)-1][1]:]) # Text after last comment
		
		#### PART 3 ####
		# This part joins text pieces, so that
		# ['ABC', 'CBA'] becomes ['ABCCBA'].
		
		data = [None]
		for x in ndata:
			if x == None:
				data.append(None)
			elif x != '':
				if data[len(data)-1] == None:
					data.append('')
				data[len(data)-1] += x
		
		data = data[1:]
		
		#### PART 4 ####
		# This part splits the text pieces into correct lines. One line in this
		# sense must only have one newline.
		
		ndata = []
		for x in data:
			if x == None:
				ndata.append(None)
			else:
				xspl = x.split('\n')
				if xspl[0] == '':
					del xspl[0]
				max = len(xspl)-1
				if xspl[max] == '':
					del xspl[max]
				ndata.extend(xspl)
		
		#### PART 5 ####
		# This part unescapes comments ('\#...' => '#...').
		escapees = '//', '#', '/*'
		for i in range(len(ndata)):
			if ndata[i] == None:
				continue
			for x in escapees:
				ndata[i] = ndata[i].replace('\\' + x, x)
		
		# Finally, make the data available for the other functions.
		self.data = ndata
	
	def get_version(self):
		"""Finds and returns version (or "doctype") and removes it from the data"""
		
		version = ''
		# Version is on the first real line.
		for i in range(len(self.data)):
			line = self.data[i]
			if line == None or line.strip() == '':
				continue
			
			self.data[i] = None # Change the version line
			version = line
			break
		
		return version
	
	def extract_data(self):
		"""Extracts raw data into groups and subgroups of data"""
		
		none_lines = []
		current_part = [''] # META or MAIN
		current_name = None # Or 'current_element/object/header'
		parts = {} # Will ultimately hold both META and MAIN
		
		i = 0
		for line in self.data:
			if line == None:
				none_lines.append(i)
				i += 1
				continue
			i += 1
			
			firsts = line.lstrip()
			
			if is_first('...', firsts) and firsts[3:] and firsts[3] != '.':
				current_part.insert(0, firsts[3:])
				if not current_part[0] in parts:
					parts[current_part[0]] = {}
				continue
			elif firsts.rstrip() == '[end]':
				current_part.pop(0)
				continue
			
			if current_part[0] == 'META' or current_part[0] == 'MAIN':
				if is_first('..', firsts) and firsts[2:] and firsts[2] != '.':
					current_name = firsts[2:].rstrip()
					if not current_name in parts[current_part[0]]:
						# Text space is prepared, line number is saved
						parts[current_part[0]][current_name] = ['', i+1]
					else:
						subpart_err(current_name, current_part[0],
						            i, parts[current_part[0]][current_name][1]-1)
					continue
				if current_name != None:
					parts[current_part[0]][current_name][0] += line + '\n'
		
		# Ignore the fact that the first line is always a "none-line"
		none_lines = none_lines[1:]
		
		if not 'META' in parts:
			parts['META'] = {}
		if not 'MAIN' in parts:
			parts['MAIN'] = {}
		
		return parts['META'], parts['MAIN'], none_lines
	
	def group_meta_data(self, meta, none_lines):
		"""Organizes the data found in the META part of movact raw data"""
		
		# Improve meta settings
		points_line = 0 # Has its special purposes; see below.
		for x in meta.items():
			text = x[1][0][:-1] # Remove last newline
			header = x[0]
			line = x[1][1]
			
			# This piece of code is for those parts that only accept Python
			# lists or tuples.
			parts_in_need = 'points', 'confirmed'
			if header in parts_in_need:
				if text:
					temp_text = text[:]
					offset = 0
					orig_line = line+0
					# Scroll through empty lines
					while temp_text[0] == '\n':
						text = text[1+offset:]
						temp_text = temp_text[1:]
						line += 1
						offset = 0
						# Check if the line only has spaces. If that's the case,
						# consider the line empty.
						while temp_text[0] == ' ':
							temp_text = temp_text[1:]
							offset += 1
					
					for y in none_lines:
						if y <= line+1 and y >= orig_line-1:
							# If none-lines exist after the part begins
							# but before it reaches this line
							line += 1
				
				if header == 'points':
					points_line = line+0 # Has its special purposes; see below.
				
				try:
					lst = eval(text)
					if isinstance(lst, list) or isinstance(lst, tuple):
						meta[header] = lst
					else:
						del meta[header]
						raise
				except:
					syntax_err(text, header, 'meta', line)
			else:
				text = text.rstrip()
				# Unescape '\..' lines (indentation allowed, so regex used)
				text = re.sub(r'\n(\s*)\\\.\.', '\\n\\1\.\.', '\n' + text)[1:]
				text = unescape_eot_specials(text)
				
				meta[header] = text
		
		# Temporarily fill in values for all available settings
		meta = base_on(meta)
		
		# Nicer
		meta['points'] = tuple(meta['points'])
		
		# Transform to lower case
		meta['confirmed'] = list(meta['confirmed'])
		for i in range(len(meta['confirmed'])):
			meta['confirmed'][i] = meta['confirmed'][i].lower()
		meta['confirmed'] = tuple(meta['confirmed'])
		
		# Check for problems
		not_to_be_overwritten = (
			meta['quit command'   ],
			meta['load command'   ],
			meta['save command'   ],
			meta['back command'   ],
			meta['current command']
		)
		for x in meta['points']:
			for y in x[1]:
				if y in not_to_be_overwritten:
					err('Error: "' + y + '" in meta.points on line ' + str(points_line) + ' cannot be used as a point, as it it used as a command.')
		
		# Make data accesible by other functions
		self.meta = meta
	
	def group_main_data(self, main, none_lines):
		"""Organizes the data found in the MAIN part of movact raw data"""
		if not 'start' in main:
			err(
"""Error: No start part specified. To fix this, add something like this:

    ..start
    You are stranded on an uninhibited island. What do you do?
    .x X
    .y Y

to your data file.""")
		
		plen = len(self.meta['points'])
		for x in main.items():
			text = x[1][0][:-1] # Remove last newline
			header = x[0]
			line = x[1][1]
			orig_line = line+0
			
			text = text.rstrip() # Remove line number and trim
			text = unescape_eot_specials(text)
			
			lines_data = []
			spl = text.split('\n')
			ref_num = 0
			for y in spl:
				lstrp = y.lstrip()
				if is_first('.', lstrp) and lstrp[1:] and lstrp[1] != '.':
					# This line links to another part
					first_space = lstrp.find(' ')
					if first_space == -1:
						lstrp += ' '
						first_space = lstrp.find(' ')
						last_first_space = first_space
					else:
						last_first_space = first_space
						while lstrp[last_first_space+1] == ' ':
							last_first_space += 1
					ref = lstrp[1:first_space]
					if not ref in main:
						# If the part doesn't exist, find the current line and
						# throw an error.
						cline = line+0
						for y in none_lines:
							if y <= cline+1 and y >= orig_line-1:
								cline += 1
						reference_err(ref, header, 'main', cline)
					else:
						reftxt = lstrp[last_first_space+1:]
						if reftxt[:1] == '\\':
							reftxt = reftxt[1:]
						lines_data.append((False, ref, reftxt))
						ref_num += 1
				else:
					if is_first('\.', lstrp):
						y = y.replace('\.', '.', 1)
					lines_data.append((True, y))
				line += 1
			
			# ^ An item in lines_data starts with True if it's a normal text
			# line, or False, if it's a pointer line.
			
			if ref_num > plen:
				err('Error: '+str(ref_num)+' points needed in main.'+header+' on line '+str(orig_line-1)+', but only '+str(plen)+' points in meta.points')
			
			lines_data.insert(0, ref_num > 0)
			lines_data.insert(0, orig_line - 1)
			main[header] = lines_data
			
			# Make data accesible by other functions
			self.main = main
	
	def look_for_non_referenced_parts(self):
		"""Checks if any parts are not referenced by other parts"""
		
		# Knowing that all movact stories start at a part named 'start', looking
		# through all references in 'start', and then looking through all
		# references in parts pointed to by 'start', and so on, will result in
		# getting a list of parts that one is able to get to from 'start'.
		
		refs = self.look_for_nrp_recursively('start', ['start'])
		
		for x in self.main.items():
			name = x[0]
			line = x[1][0]
			if name not in refs:
				non_reference_err(name, 'main', line)
			
	def look_for_nrp_recursively(self, part, refs):
		"""Calls itself recursively to check for references"""
		for x in self.main[part][2:]:
			if not x[0] and x[1] not in refs:
				refs.append(x[1])
				refs = self.look_for_nrp_recursively(x[1], refs)
		return refs
	
	def print_lines(self):
		"""Prints the half-processed lines of data for debugging purposes"""
		l = len(self.data)
		sl = len(str(l))
		for i in range(l): print (sl-len(str(i+1)))*'0'+str(i+1), self.data[i]
	
	def get_game_data(self):
		"""Returns a tuple of game data"""
		return self.meta, self.main
	
	def pickle_game_data(self):
		"""Pickles the game data and returns the output"""
		txt = pickle.dumps(self.get_game_data())
		return '#!/usr/bin/env movact\n# You can add your own comments here.\n\n' + txt
	
	def unpickle_game_data(self):
		"""Unpickles the game data and applies the output to the game"""
		
		txt = self.data[:]
		# Remove '#' comments and empty lines
		txt = txt.split('\n')
		while txt[0].lstrip()[:1] in ('#', ''):
			del txt[0]
		txt = '\n'.join(txt)
		
		# Unpickle text data
		try:
			data = pickle.loads(txt)
			self.meta = data[0]
			self.main = data[1]
			return True
		except Exception, erred:
			python_err(erred)
		except:
			unknown_err(details=erred)
