# required imports
import openCV
import numpy as np
import inputModule
import imageprocessingModule

class Event(object):
	"""docstring for Event"""
	def __init__(self, arg, roi):
		super(Event, self).__init__()
		self.arg = arg
		self.roi = roi

		
class ObjectRemoval(Event):
	"""docstring for Event1"""
	def __init__(self, arg):
		super(Event1, self).__init__()
		self.arg = arg

class Event2(Event):
	"""docstring for Event2"""
	def __init__(self, arg):
		super(Event2, self).__init__()
		self.arg = arg
		
class Event3(Event):
	"""docstring for Event3"""
	def __init__(self, arg):
		super(Event3, self).__init__()
		self.arg = arg
		
