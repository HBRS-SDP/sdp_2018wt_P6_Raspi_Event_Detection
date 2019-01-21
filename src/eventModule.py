# required imports
import cv2
import numpy as np
import inputModule
import imageprocessingModule as ip
import datetime

class Event(object):
	"""docstring for Event"""
	def __init__(self, roi, events):
		super(Event, self).__init__()
		# initializing list of lists for roi
		self.roi = roi
		self.avg = None
		self.ip = ip
		self.preproc = self.ip.Preprocess()
		self.ef = self.ip.Extractfeatures()
		self.trigger = False
		self.track_grasp = 0
		self.track_release = 0
		self.previous_state = None
		self.motion_flag = None
		self.original_frame = None
		self.object_info = {}
		self.res = {}
		self.frame_number = 1
		self.events = events

	def eventManager(self, frame, segment, roi):
		self.res = {}
		if self.frame_number == 1:
			self.num_objects, dict_, self.mask_original = self.ef.find_all_objects(frame, segment, self.object_info, roi)
			self.original_frame = frame
			self.frame_number += 1
		self.num, d_, self.new_mask = self.ef.find_all_objects(frame, segment, self.object_info, roi)
		self.motion_flag = self._motion_trigger(self.new_mask, self.mask_original)
		print("[PRINT] Motion Flag: {}".format(self.motion_flag))
		if self.motion_flag == True:
			self.mask_original = self.new_mask

		# Check grasp
		if "grasp" in self.events:
			self.grasp_flag, self.track_grasp = self._check_grasp(self.num, self.num_objects, self.track_grasp)
			if self.track_grasp > 3:
				self.track_grasp = 0
				print("[INFO]: Object Grasped")
				self.res["data"] = []
				#self.res["data"]["event"] = []
				timing = datetime.datetime.now()
				self.res["data"].append(["Object Grasp", (str(timing.year)+"/"+str(timing.month)+"/"+ str(timing.day),\
					str(timing.hour)+"."+str(timing.minute)+"."+str(timing.second))])
				self.num_objects = self.num
				self.previous_state = "grasp"

		# Check Release
		if "release" in self.events:
			self.release_flag, self.track_release = self._check_release(self.num, self.num_objects, self.track_release)
			if self.track_release > 3:
				self.track_release = 0
				print("[INFO]: Object Released")
				self.res["data"] = []
				timing = datetime.datetime.now()
				self.res["data"].append(["Object Release", (str(timing.year)+"/"+str(timing.month)+"/"+ str(timing.day),\
					str(timing.hour)+"."+str(timing.minute)+"."+str(timing.second))])
				self.num_objects = self.num
				self.previous_state = "release"

		if self.previous_state in ["grasp", "release"] and self.motion_flag == False:

				if self.previous_state == "grasp":
					print("[INFO]: Object Removed")
					timing = datetime.datetime.now()
					if "object_removal" in self.events:
						self.res["data"] = []
						self.res["data"].append(["Object Removed", (str(timing.year)+"/"+str(timing.month)+"/"+ str(timing.day),\
							str(timing.hour)+"."+str(timing.minute)+"."+str(timing.second))])
			
				elif self.previous_state == "release":
					print("[INFO]: Object Introduced")
					timing = datetime.datetime.now()
					if "object_introduction" in self.events:
						self.res["data"] = []
						self.res["data"].append(["Object Introduced", (str(timing.year)+"/"+str(timing.month)+"/"+ str(timing.day),\
							str(timing.hour)+"."+str(timing.minute)+"."+str(timing.second))])
				self.previous_state = None

		return self.res


	def _motion_trigger(self, mask1, mask2):
		"""
		Trigger Responsible for events (if motion)

		Returns: Boolean (true/false)
		Initializes: grasp, release

		"""
		frameDelta = cv2.absdiff(mask1, mask2)
		nonzeros = cv2.countNonZero(frameDelta)
		print("[INFO]: Difference Value is {}".format(nonzeros))
		if nonzeros > 600:
			return True
		else:
			return False

	def _check_grasp(self, num1, num2, track_grasp):
		"""
		If there is motion, check if there is something common between initial frame and current mask

		Returns: Boolean (True/ False)
		"""
		if num1 < num2:
			track_grasp += 1
			return True, track_grasp
		else:
			return False, track_grasp

	def _check_release(self, num1, num2, track_release):
		"""
		If there is motion, check if there is something common between initial frame and current mask

		Returns: Boolean (True/ False)
		"""
		if num1 > num2:
			track_release += 1
			return True, track_release
		else:
			return False, track_release