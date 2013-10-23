# galene $Id: Output.py 22 2012-02-27 23:57:19Z zephyr $
#
# Copyright (c) 2012 Vita Smid <me@ze.phyr.us>

class Output:
	'''
	Single-point output filter with configurable verbosity levels.
	'''

	ERR = 1		# error
	WARN = 2	# warning
	NOTICE = 3
	DEBUG = 4


	def __init__(self, level, stream = None):
		self.level = level
		if stream is None:
			import sys
			stream = sys.stderr
		self.stream = stream


	def __call__(self, level, msg, *args):
		'''
		@param msg: The message to we written.
		@param args: Optional format parameters to the message.
		'''
		if level <= self.level:
			print >>self.stream, msg % args
