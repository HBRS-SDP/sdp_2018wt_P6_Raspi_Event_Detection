# required imports
import cv2
import numpy as np
import sys
import configparser
# from picamera.array import PiRGBArray
# from picamera import PiCamera

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
		if sys.argv[1] not in ["pc", "pi", "video"]:
			print("[ERR]: The specified mode does not exists")
			sys.exit(0)
		else:
			self.mode = sys.argv[1]
		if self.mode == "video":
			self.stream_init = Stream(self.mode, sys.argv[2])
		else:
			self.stream_init = Stream(self.mode)
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
		if self.mode == "pi":
			frame = self.cap.capture(PiRGBArray(self.cap), format="bgr")
			frame = frame.array
		else:
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
		if self.device == "video":
			self.capture = cv2.VideoCapture(self.videosource)
		elif self.device == "pc":
			self.capture = cv2.VideoCapture(self.videosource)
		else:
			self.capture = PiCamera()
			self.capture.resolution = [640,480]
			self.capture.framerate = 7
			
		return self.capture
