# required imports
import cv2
import numpy as np
import inputModule

class Preprocess(object):
	"""
	-----------------------------------------
	Basic preprocessing, grayscale conversion,
	Binarization etc.

	Input: Frame from input module
	output: Transformed image, numpy ndarray
	-----------------------------------------
	"""
	def __init__(self):
		super(Preprocess, self).__init__()

		# initialize the input module
		self.init_input = inputModule.VideoHandler()
		# fetch the frame
		self.color_frame = self.init_input.get_current_frame()

	def convert_to_other_color_space(space = "gray"):
		if space == "gray":
			self.transformed_frame = cv2.cvtColor(self.color_frame, cv2.COLOR_BGR2GRAY)

		return self.transformed_frame

class Extractfeatures(object):
	"""docstring for Extractfeatures"""
	def __init__(self, arg):
		super(Extractfeatures, self).__init__()
		self.arg = arg
		
class Postprocess(object):
	"""
	--------------------------------------
	Once the features are extracted,
	post process on the ROI and get the
	desired event response.

	Input: Keypoints, image
	Output: Transformed Image
	--------------------------------------
	"""
	def __init__(self, arg):
		super(Postprocess, self).__init__()
		self.arg = arg

"""
---------------------------------
Write the unit testing for this code
---------------------------------
"""

if __name__ == '__main__':
	try:
		pp = Preprocess()
	except Exception as e:
		raise e