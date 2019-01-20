# required imports
import cv2
import numpy as np
import sys
import configparser

###
"""
config = configparser.ConfigParser()
cfg = config.read('config.ini')
cfg['paths']
"""
###

class VideoHandler(object):
	"""
	Notes for this class
	-----------------------------------

	expects: Video capture object
	library used: openCV
	returns: frames
	-----------------------------------
	"""
	def __init__(self):
		super(VideoHandler, self).__init__()
		self.stream_init = Stream("pc", sys.argv[1])
		self.cap = self.stream_init.init_stream()

		# Build and exception if the video source is None
		if not self.cap.isOpened():
			print("There video source doesn't exist")
			sys.exit(1)

	def get_current_frame(self):
		"""
		--------------------------------
		used to get current frame from the 
		given video source. 

		Returns: Frame
		Format: numpy ndarray
		---------------------------------
		"""
		_, frame = self.cap.read()
		return frame

class Stream(object):
	"""
	Notes for this class
	--------------------------------------
	expects: Video source
	library used: openCV
	returns: Video capture object
	--------------------------------------
	"""
	def __init__(self, device = "pc", videosource = 0):
		super(Stream, self).__init__()
		self.device = device
		self.videosource = videosource

	def init_stream(self):
		if self.device == "pc":
			self.capture = cv2.VideoCapture(self.videosource)
		else:
			self.capture = None
		return self.capture
