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

                            ######################
                            ## GTK GUI frontend ##
                            ######################
#############
## IMPORTS ##
#############
## Global
import sys
from os.path import realpath, dirname
import pygtk
pygtk.require('2.0') # In reality 2.6
import gtk
try:
	# In any 'About' window, doing this will make it possible to click on links
	from gnome import url_show
	def show_url(d, link, x):
		url_show(link)
	def show_email(d, link, x):
		url_show('mailto:' + link)
	gtk.about_dialog_set_url_hook(show_url, True)
	gtk.about_dialog_set_email_hook(show_email, True)
except:
	pass

## Local
from movactorg.core.run import *

#####################################################
HELPTEXT = '\nThis is the GUI frontend using GTK.' ##
#####################################################
VERSIONTEXT = """\
movact-gtk 0.5
Copyright (C) 2009  Niels Serup <ns@metanohi.org>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.\
"""

CONTENT_SIZE	 = 500 , 300 # Width and height of content
SCROLLBARS_EXTRA =  60 ,  30 # Extra width and height available for scrollbars


######################
## CLASS DEFINITION ##
######################
class Label(gtk.Label):
	"""Creates a gtk label, then modifies it"""
	def __init__(self, txt = '', width = CONTENT_SIZE[0]):
		gtk.Label.__init__(self, txt)
		self.set_line_wrap(True)
		self.set_size_request(width, -1)

class Runner(GenericRunner):
	def __init__(self, **args):
		self.path = dirname(realpath(__file__)) + '/../../../'
		
		# GTK-specific
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", lambda *w: gtk.main_quit())
		self.window.set_border_width(2)
		self.window.set_title("movact")
		self.window.set_icon_from_file(self.path + 'art/movact-logo-64.png')
		
		# Create contents containers
		wrapper = gtk.HBox(False, 5)
		self.window.add(wrapper)
		
		l_box = gtk.VBox(False, 5)
		m_box = gtk.VBox(False, 5)
		r_box = gtk.VBox(False, 5)
		
		wrapper.pack_start(l_box, False, False, 0)
		wrapper.pack_end(r_box, False, False, 0)
		wrapper.pack_end(m_box, False, False, 0)
		
		content_scrollbars = gtk.ScrolledWindow()
		self.infotext = Label('...', CONTENT_SIZE[0] + SCROLLBARS_EXTRA[0])
		l_box.pack_start(content_scrollbars, False, False, 0)
		l_box.pack_start(self.infotext, False, False, 0)
		
		self.c_box = gtk.VBox(False)		
		content_scrollbars.add_with_viewport(self.c_box)
		
		m_box.pack_start(gtk.VSeparator())
		
		# General stuff
		GenericRunner.__init__(self, **args)
		
		# Buttons to the right
		open_button = gtk.Button(self.meta['open button'])
		self.back_button = gtk.Button(self.meta['back button'])
		self.reset_button = gtk.Button(self.meta['reset button'])
		self.load_button = gtk.Button(self.meta['load button'])
		self.save_button = gtk.Button(self.meta['save button'])
		quit_button = gtk.Button(self.meta['quit button'])
		about_button = gtk.Button('About')
		
		open_button.connect('clicked', self.prepare_open)
		self.back_button.connect('clicked', self.back)
		self.reset_button.connect('clicked', self.reset)
		self.load_button.connect('clicked', self.prepare_load)
		self.save_button.connect('clicked', self.prepare_save)
		quit_button.connect('clicked', self.quit)
		about_button.connect('clicked', self.show_about)
		
		r_box.pack_start(open_button, False, False, 0)
		r_box.pack_start(gtk.HSeparator(), False, False, 0)
		r_box.pack_start(self.back_button, False, False, 0)
		r_box.pack_start(self.reset_button, False, False, 0)
		r_box.pack_start(self.load_button, False, False, 0)
		r_box.pack_start(self.save_button, False, False, 0)
		r_box.pack_start(quit_button, False, False, 0)
		r_box.pack_start(gtk.HSeparator(), False, False, 0)
		r_box.pack_start(about_button, False, False, 0)
		
		content_scrollbars.set_policy(
		    gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		content_scrollbars.set_size_request(
		    CONTENT_SIZE[0] + SCROLLBARS_EXTRA[0],
		    CONTENT_SIZE[1] + SCROLLBARS_EXTRA[1])
		
		# Automatically unpickle an opened file when its filename ends on
		# '.pickled'? (can be changed in a FileChooserDialog withing the
		# program, see prepare_open
		self.autounpickle_on = True
		
		if not self.ok:
			self.back_button.set_sensitive(False)
			self.reset_button.set_sensitive(False)
			self.load_button.set_sensitive(False)
			self.save_button.set_sensitive(False)
		
		self.window.show_all()
		self.window.set_resizable(False)
		
		self.story_done = False
		if self.ok:
			self.start()
		
		gtk.main()
	
	def start(self):
		"""Prints startup message and runs game"""
		if self.meta['start-gui']:
			self.c_box.pack_start(Label(self.meta['start-gui']))
			self.c_box.pack_start(gtk.HSeparator())
		
		self.run(False)
	
	def goto(self, b, part_name):
		self.part_name = part_name
		self.run()
	
	def run(self, remove_elements = True):
		"""Runs a movact game part"""
		if remove_elements:
			for x in self.c_box.get_children():
				self.c_box.remove(x)
		
		part = self.main[self.part_name]
		refs_num = 0
		text = ''
		for x in part[1:]:
			# A line can either become a piece of text or a button. If it's
			# text, add it to former text; if it's a button, print the text and
			# add the button.
			if x[0]:
				text += x[1] + '\n'
			else:
				if text != '':
					text = text[:-1]
					self.c_box.pack_start(Label(text))
					text = ''
				
				p = self.meta['points'][refs_num]
				button = gtk.Button(p[0] + x[2])
				button.connect('clicked', self.goto, x[1])
				self.c_box.pack_start(button, False, False, 0)
				refs_num += 1
		
		if text != '':
			text = text[:-1]
			self.c_box.pack_start(Label(text))
		
		if len(self.visited_parts) == 0:
			self.back_button.set_sensitive(False)
			self.reset_button.set_sensitive(False)
		else:
			self.back_button.set_sensitive(True)
			self.reset_button.set_sensitive(True)
		
		self.visited_parts.append(self.part_name)
		self.infotext.set_text(
		    '"'+self.part_name+'" (' + str(len(self.visited_parts)-1) + ')')
		self.autosave()
		
		self.story_done = False
		if not part[0]:
			# If last
			self.c_box.pack_start(gtk.HSeparator())
			self.c_box.pack_start(Label(self.meta['end-gui']))
			self.story_done = True
		
		# Important
		self.window.show_all()
	
	def back(self, b = None):
		"""Goes one step back, if possible"""
		if len(self.visited_parts) > 1:
			self.visited_parts.pop()
			self.part_name = self.visited_parts[-1]
			self.visited_parts.pop()
			self.run()
		else:
			self.infotext.set_text(self.meta['error'])
	
	def reset(self, b = None):
		"""Resets state completely"""
		if self.confirmed():
			self.part_name = self.visited_parts[0]
			self.visited_parts = []
			self.run()
	
	def confirmed(self, msg = None):
		"""Asks the user if they are sure"""
		if self.story_done or not self.ok:
			return True # No need to ask a user for permission to do something
			            # when he has finished a game.
		
		if msg == None:
			msg = self.meta['confirm-gui']
		dialog = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL,
								   gtk.MESSAGE_QUESTION,
								   gtk.BUTTONS_YES_NO, msg)
		result = dialog.run()
		dialog.destroy()
		return result == gtk.RESPONSE_YES
	
	def prepare_open(self, b = None):
		"""Asks the user to choose a file"""
		dialog = gtk.FileChooserDialog(self.meta['open-gui'],
									   self.window,
									   gtk.FILE_CHOOSER_ACTION_OPEN,
										 (
										  gtk.STOCK_CANCEL,
										  gtk.RESPONSE_CANCEL,
										  gtk.STOCK_OPEN,
										  gtk.RESPONSE_OK
										 )
									   )
		
		detect = gtk.CheckButton(
'Automatically detect pickled files based on their filenames (*.pickled).')
		detect.set_active(self.autounpickle_on)
		detect.connect('clicked', self.change_autounpickle)
		detect.show()
		
		dialog.set_extra_widget(detect)
		
		dialog.set_default_response(gtk.RESPONSE_OK)
		
		f = False
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			name = dialog.get_filename()
			if self.open(name, self.autounpickle_on):
				self.infotext.set_text(self.meta['opened'])
				self.back_button.set_sensitive(True)
				self.reset_button.set_sensitive(True)
				self.load_button.set_sensitive(True)
				self.save_button.set_sensitive(True)
				for x in self.c_box.get_children():
					self.c_box.remove(x)
				self.start()
				
				f = True
			else:
				self.infotext.set_text(self.meta['error'])
				f = False
		
		dialog.destroy()
		return f
	
	def prepare_load(self, b = None):
		"""Asks the user to choose a file"""
		dialog = gtk.FileChooserDialog(self.meta['load-gui'],
									   self.window,
									   gtk.FILE_CHOOSER_ACTION_OPEN,
									   (
										  gtk.STOCK_CANCEL,
										  gtk.RESPONSE_CANCEL,
										  gtk.STOCK_OPEN,
										  gtk.RESPONSE_OK)
									   )
		dialog.set_default_response(gtk.RESPONSE_OK)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			name = dialog.get_filename()
			if self.load(name):
				self.run()
		
		dialog.destroy()
	
	def load(self, filename, err = True):
		l = GenericRunner.load(self, filename, err)
		if l:
			self.infotext.set_text(self.meta['loaded'])
			return True
		elif err:
			self.infotext.set_text(self.meta['load error'])
			return False
	
	def prepare_save(self, b = None):
		"""Asks the user to choose a file"""
		dialog = gtk.FileChooserDialog(self.meta['save-gui'],
									   self.window,
									   gtk.FILE_CHOOSER_ACTION_SAVE,
									   (
										  gtk.STOCK_CANCEL,
										  gtk.RESPONSE_CANCEL,
										  gtk.STOCK_SAVE,
										  gtk.RESPONSE_OK)
									   )
		dialog.set_default_response(gtk.RESPONSE_OK)

		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			name = dialog.get_filename()
			self.save(name)
		
		dialog.destroy()
	
	def save(self, filename, mention = True):
		s = GenericRunner.save(self, filename, mention)
		if s and mention:
			self.infotext.set_text(self.meta['saved'])
	
	def quit(self, b = None):
		"""Exits"""
		if self.confirmed():
			gtk.main_quit()
	
	def show_about(self, b = None):
		dialog = gtk.AboutDialog()
		dialog.set_title('About movact-gtk')
		dialog.set_version('0.5')
		dialog.set_copyright('Copyright © 2009 Niels Serup')
		dialog.set_license("""\
movact-gtk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

movact-gtk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with movact-gtk.  If not, see <http://www.gnu.org/licenses/>.\
""")
		dialog.set_website('http://metanohi.org/projects/movact/')
		dialog.set_website_label('movact website')
		dialog.set_program_name('movact-gtk')
		dialog.set_authors(('Niels Serup <ns@metanohi.org>',))
		dialog.set_documenters(('Niels Serup <ns@metanohi.org>',))
		dialog.set_artists(('Niels Serup <ns@metanohi.org>',))
		dialog.set_logo(
		    gtk.gdk.pixbuf_new_from_file(self.path+'art/movact-logo-256.png'))
		dialog.set_icon_from_file(self.path + 'art/movact-logo-64.png')
		
		dialog.run()
		dialog.destroy()
	
	def change_autounpickle(self, b):
		self.autounpickle_on = not self.autounpickle_on
