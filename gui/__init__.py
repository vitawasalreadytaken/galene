# galene
# 
# Copyright (c) 2012-2013 Vita Smid <http://ze.phyr.us>

import gtk, gtksourceview2, pygtk, pango
from Window import Window


def init(config, files):
	window = Window(config)
	
	if len(files):
		window.open(files[0]) # We open no more than one file.

	window.show()

