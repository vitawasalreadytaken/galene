# galene $Id: __init__.py 23 2012-02-28 00:04:59Z zephyr $
# 
# Copyright (c) 2012 Vita Smid <me@ze.phyr.us>

import gtk, gtksourceview2, pygtk, pango
from Window import Window


def init(config, files):
	window = Window(config)
	
	if len(files):
		window.open(files[0]) # We open no more than one file.

	window.show()

