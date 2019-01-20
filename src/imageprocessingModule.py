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
		pass

	def convert_to_other_color_space(self, frame, space = "gray"):
		if space == "gray":
			self.transformed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		return self.transformed_frame

	def blur(self, frame):
		gray = cv2.GaussianBlur(frame, (21, 21), 0)
		return gray


class Extractfeatures(object):
	"""docstring for Extractfeatures"""
	def __init__(self):
		#super(Extractfeatures, self).__init__()
		self.random_int = 1

	def find_all_objects(self,frame, segment, objects_info, roi):
		gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,100,200)
		dialated = cv2.dilate(edges, None, iterations=8)
		h = segment.shape[0]
		w = segment.shape[1]
		_, contours, hierarchy = cv2.findContours(dialated.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		i = 0
		for c in contours:
			if 500 < cv2.contourArea(c) < 10000:
				(x, y, w, h) = cv2.boundingRect(c)
				new_dilation = cv2.dilate(dialated[y:y+h,x:x+w], None, iterations=5)
				dialated[y:y+h,x:x+w] = new_dilation
		_, contours, hierarchy = cv2.findContours(dialated.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		for p in contours:
			if 3000 < cv2.contourArea(p) < 8000:
				objects_info[i] = {}
				(x,y,w,h) = cv2.boundingRect(p)
				x = x + roi[0][0]
				y = y + roi[0][1]
				objects_info[i]["center"] = (int(x+w/2), int(y+h/2))
				cv2.rectangle(frame,(int(x),int(y)),(int(x+w), int(y+h)), (0, 255, 0), 2)
				i += 1
		print("[INFO] Model Init, {} objects found".format(i))
		return i, objects_info, dialated


		
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
