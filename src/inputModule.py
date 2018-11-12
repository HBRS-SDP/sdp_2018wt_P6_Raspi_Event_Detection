# required imports
import cv2
import numpy as np

class VideoHandler(object):
	"""
	Notes for this class
	-----------------------------------

	expects: Video capture object
	library used: openCV
	returns: frames
	-----------------------------------
	"""
	def __init__(self, arg):
		super (VideoHandler, self).__init__()
		self.arg = arg

class Stream(object):
	"""
	Notes for this class
	--------------------------------------
	expects: Video source
	library used: openCV
	returns: Video capture object
	--------------------------------------
	"""
	def __init__(self, arg):
		super(Stream, self).__init__()
		self.arg = arg
		
