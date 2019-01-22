# required imports
import cv2
import numpy as np
import inputModule
import imageprocessingModule

class Event(object):
	"""docstring for Event"""
	def __init__(self, roi):
		super(Event, self).__init__()
		# initializing list of lists for roi
		self.roi = roi
		self.avg = None
		self.ip = imageprocessingModule()
		self.preproc = self.ip.preprocess()
		self.trigger = False
		self.res = {}

	def _motiontrigger(self,frame):
		# This will trigger all the events to check if they have occured
		self.gray_frame = self.preproc.convert_to_other_color_space(frame)
		self.blurred_frame = self.preproc.blur(self.gray_frame)
		if self.avg is None:
			print("[INFO] Starting Background model")
			self.avg = self.blurred_frame.copy().astype("float")
		cv2.accumulateWeighted(self.blurred_frame, self.avg, 0.7)
		frameDelta = cv2.absdiff(self.blurred_frame, cv2.convertScaleAbs(self.avg))
		thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		for c in contours:
			if cv2.contourArea(c) > conf["min_area"]:
				self.trigger = True
				(x, y, w, h) = cv2.boundingRect(c)
				# Spawn other motion based events
				_or = ObjectRemoval(thresh)
				removal_status = _or.checkifremoved([x,y,x+w/2, y+h/2],[roi[0],roi[1],roi[0]+roi[2]/2,roi[1]+roi[3]/2])
				if removal_status == True:
					self.res["object_removal"] = {}
					self.res["object_removal"]["status"] = True
				# Spawn event2


		removal_status = False
		return self.res


class ObjectRemoval(Event):
	"""docstring for Event1"""
	def __init__(self, frame):
		super(Event1, self).__init__()
		self.motion_frame = frame

	def checkifremoved(self, boxA, boxB):
		xA = max(boxA[0], boxB[0])
		yA = max(boxA[1], boxB[1])
		xB = min(boxA[2], boxB[2])
		yB = min(boxA[3], boxB[3])

		interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
		boxAArea = (x+w - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
		boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
		iou = interArea / float(boxAArea + boxBArea - interArea)

		if iou < 0.3:
			return True
		else:
			return False

# class Event2(Event):
# 	"""docstring for Event2"""
# 	def __init__(self, arg):
# 		super(Event2, self).__init__()
# 		self.arg = arg
		
# class Event3(Event):
# 	"""docstring for Event3"""
# 	def __init__(self, arg):
# 		super(Event3, self).__init__()
# 		self.arg = arg
		
