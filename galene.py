#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# γαλήνη (galene) 
# Copyright (c) 2012-2013 Vita Smid <http://ze.phyr.us>
# Licensed under the terms of The MIT License. 



CONFIG = {
	# Color scheme for gtktextview2.
	'scheme': 'oblivion',

	# Window backround color. Used only when background color from the scheme cannot be used.
	'background': '#fff',
	
	# Font used for the editor.
	'font': 'LMRoman12 14',
	
	# Width of the text editor relative to the window.
	'textWidth': 0.618
}


###############################################################################
import optparse, os, sys
import gtk, gtksourceview2, pygtk, pango

import gui, utils
from utils import out

class Galene:
	OPTIONS = (
		optparse.make_option('-v', '--verbose', action = 'count', dest = 'verbosity', default = 1),
		optparse.make_option('-q', '--quiet', action = 'store_const', dest = 'verbosity', const = 0)
	)


	def parseArgs(self, argv):
		parser = optparse.OptionParser(option_list = self.OPTIONS)
		(options, positional) = parser.parse_args(argv)
		return (options, positional)


	def __init__(self):
		progDir = os.path.dirname(sys.argv[0])
		(self.args, files) = self.parseArgs(sys.argv[1:])
		out.level = self.args.verbosity
		out(out.DEBUG, 'Parsed arguments: %s', self.args)
		self.config = CONFIG
		gui.init(self.config, files)


	def main(self):
		try:
			gtk.main()
		except KeyboardInterrupt:
			out(out.NOTICE, 'Caught keyboard interrupt, quitting')



if __name__ == '__main__':
	app = Galene()
	app.main()

