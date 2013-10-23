# -*- coding: UTF-8 -*-
# galene $Id: Window.py 28 2012-05-04 12:15:12Z zephyr $
# 
# Copyright (c) 2012 Vita Smid <me@ze.phyr.us>

import gtk, gtksourceview2, pygtk, pango
import os, sys

class Window(gtk.Window):

	def getAccels(self):
		return {
			'<Control>s': self.save,
			'<Shift><Control>s': self.saveAs,
			'<Control>o': self.openDialog,
			'<Control><Alt>e': lambda: self.addTag('em'),
			'<Control><Alt>p': lambda: self.addTag('p'),
			'<Control><Alt>g': lambda: self.addTag('strong'),
			'<Control><Alt>c': self.comment,
			'<Control>space': lambda: self.insert('&nbsp;')
		}


	def __init__(self, config):
		super(Window, self).__init__(gtk.WINDOW_TOPLEVEL)
		
		self.fileName = None
		self.config = config

		manager = gtksourceview2.StyleSchemeManager()
		scheme =  manager.get_scheme(config['scheme'])
		backgroundColor = gtk.gdk.color_parse(scheme.get_style('text').get_property('background') if scheme else config['background'])

		self.set_border_width(0)
		self.set_default_size(700, 500)
		self.modify_bg(gtk.STATE_NORMAL, backgroundColor)

		self.buffer = gtksourceview2.Buffer()
		self.buffer.set_highlight_matching_brackets(False)
		self.buffer.connect('modified-changed', self.onChange)
		if scheme:
			self.buffer.set_style_scheme(scheme)

		self.view = gtksourceview2.View(self.buffer)
		self.view.set_wrap_mode(gtk.WRAP_WORD_CHAR)
		self.view.set_justification(gtk.JUSTIFY_FILL)
		self.view.modify_base(gtk.STATE_NORMAL, backgroundColor)

		vbox = gtk.VBox(spacing = 0)
		
		self.label = gtk.Label()
		self.label.set_justify(gtk.JUSTIFY_LEFT)
		self.label.set_alignment(0, .5)
		self.label.set_ellipsize(pango.ELLIPSIZE_MIDDLE)

		font = pango.FontDescription(config['font'])
		if font:
			self.label.modify_font(font)
			self.view.modify_font(font)

		
		vbox.pack_start(self.label, expand = False, padding = 10)

		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		sw.add(self.view)

		vbox.pack_end(sw, padding = 10)
		
		self.add(vbox)
		
		self.connect('expose-event', self.onResize)
		self.connect('delete-event', self.onClose)
		self.setTitle()

		ag = gtk.AccelGroup()
		for spec in self.getAccels().keys():
			(key, mod) = gtk.accelerator_parse(spec)
			ag.connect_group(key, mod, gtk.ACCEL_LOCKED, self.handleAccelerator)
		
		self.add_accel_group(ag)


	def handleAccelerator(self, accelGroup, widget, key, mod):
		spec = gtk.accelerator_name(key, mod)
		self.getAccels()[spec]()


	def addTag(self, tag):
		self.wrap('<%s>' % tag, '</%s>' % tag)


	def comment(self):
		self.wrap('<!-- ', ' -->')


	def wrap(self, start, end):		
		# If there is a selection, wrap the tag around it.
		if self.buffer.get_has_selection():
			selStart = lambda: self.buffer.get_selection_bounds()[0]
			selEnd = lambda: self.buffer.get_selection_bounds()[1]
			self.buffer.insert(selStart(), start)
			self.buffer.insert(selEnd(), end)
			# We want to select back the original text, so we move the selection end back by the length of the end tag.
			bound = selEnd()
			bound.backward_chars(len(end))
			self.buffer.select_range(selStart(), bound)
		# If there's no selection, just insert the tag and place the cursor inside.
		else:
			self.buffer.insert_at_cursor(start + end)
			bound = self.buffer.get_iter_at_mark(self.buffer.get_insert())
			bound.backward_chars(len(end))
			self.buffer.place_cursor(bound)


	def insert(self, text):
		self.buffer.insert_at_cursor(text)


	def open(self, fileName):
		path = os.path.abspath(fileName)

		try:
			text = file(path).read()
		except:
			return False
		self.buffer.begin_not_undoable_action()
		self.buffer.set_text(text)
		self.buffer.end_not_undoable_action()
		
		self.buffer.set_modified(False)
		self.buffer.place_cursor(self.buffer.get_start_iter())
		self.view.set_buffer(self.buffer)
		self.fileName = fileName
		self.setHighlight()
		self.setTitle()
		return True

	
	def openDialog(self):
		if not self.checkModifiedBeforeClose():
			return False

		dialog = gtk.FileChooserDialog(parent= self, action = gtk.FILE_CHOOSER_ACTION_OPEN, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
		dialog.set_title('γαλήνη – Open file…')
		response = dialog.run()
		fileName = dialog.get_filename()
		dialog.destroy()
		if response != gtk.RESPONSE_OK or not fileName:
			return False
		
		return self.open(fileName)

	
	def setHighlight(self):
		manager = gtksourceview2.LanguageManager()
		language = manager.guess_language(self.fileName)
		if language:
			self.buffer.set_highlight_syntax(True)
			self.buffer.set_language(language)
		else:
			self.buffer.set_highlight_syntax(False)


	def setTitle(self):
		if self.fileName:
			(path, name) = os.path.split(os.path.abspath(self.fileName))
			title = '%s (%s)' % (name, path)
		else:
			title = 'Untitled'

		mod = '*' if self.buffer.get_modified() else ''

		self.set_title('%s%s – γαλήνη' % (mod, title))
		self.label.set_markup('<span color="#bbb">%s%s</span>' % (mod, title))


	def onChange(self, buffer):
		self.setTitle()
		self.present() # Should restore fullscreen mode.


	def onResize(self, win, event):
		(w, h) = self.get_size()
		margin = int(w * (1 - self.config['textWidth']) / 2)
		self.label.set_padding(margin, 0)
		self.view.set_left_margin(margin)
		self.view.set_right_margin(margin)

	
	def checkModifiedBeforeClose(self):
		'''
		If the current file is modified, ask the user whether we should save it before closing.
		Returns False when the user cancels the operation or the saving fails, True otherwise.
		'''
		
		if not self.buffer.get_modified():
			return True

		fileName = self.fileName if self.fileName else 'Untitled'
		dialog = gtk.MessageDialog(parent = self, flags = gtk.DIALOG_MODAL, type = gtk.MESSAGE_QUESTION, message_format = 'Save changes to %s?' % fileName)
		dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_YES, gtk.RESPONSE_YES)
		dialog.set_default_response(gtk.RESPONSE_YES)
		
		response = dialog.run()
		dialog.destroy()

		if response == gtk.RESPONSE_YES:
			return self.save()
		elif response == gtk.RESPONSE_CANCEL:
			return False
		else:
			return True


	def onClose(self, win, event):
		if self.checkModifiedBeforeClose():
			gtk.main_quit()
			return False
		else:
			return True


	def saveDialog(self):
		dialog = gtk.FileChooserDialog(parent= self, action = gtk.FILE_CHOOSER_ACTION_SAVE, buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
		dialog.set_title('γαλήνη – Save as…')
		if self.fileName:
			dialog.set_filename(self.fileName)
		response = dialog.run()
		fileName = dialog.get_filename()
		dialog.destroy()
		if response != gtk.RESPONSE_OK or not fileName:
			return False
		else:
			return fileName


	def saveAs(self):
		fileName = self.saveDialog()
		if not fileName:
			return False
		self.fileName = fileName
		self.save()


	def save(self):
		if not self.fileName:
			fileName = self.saveDialog()
			if not fileName:
				return False
			self.fileName = fileName
		
		text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
		try:		
			file(self.fileName, 'w').write(text)
		except:
			dialog = gtk.MessageDialog(parent = self, flags = gtk.DIALOG_MODAL, type = gtk.MESSAGE_ERROR, buttons = gtk.BUTTONS_CLOSE, message_format = 'Error saving %s!' % self.fileName)
			dialog.run()
			dialog.destroy()
			return False
		
		self.buffer.set_modified(False)
		self.setTitle()
		self.setHighlight()
		return True


	def show(self):
		self.show_all()
		self.fullscreen()

