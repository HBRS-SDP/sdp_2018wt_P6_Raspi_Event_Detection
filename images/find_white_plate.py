"""
Coded by: Harsh Munshi
Company: Graymatics INC
"""

import cv2
import numpy as np 
import sys

"""
The code assumes a cropped image for alignment. Since the number plates all around the world are different we initally
categorize them as 3 probable types:
1. White plate with black characters
2. Black plate with white characters
3. Yellow plates with black characters
"""

class Findextrema:

	def __init__(self, image):
		self.frame = image
		self.sensitivity = 120

	def findextremepoints(self):
		"""
		This function does the following task:
		1. Convert RGB to HSV
		2. Mask out all the "white" regions.
		3. Find out the Largest connected white region and return the image
		"""
		self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

		# Define upper and lower bounds for white color
		lower_white = np.array([0,0,255-self.sensitivity], dtype=np.uint8)
		upper_white = np.array([255,self.sensitivity,255], dtype=np.uint8)
		mask = cv2.inRange(self.hsv, lower_white, upper_white)
		self.res = cv2.bitwise_and(self.frame,self.frame, mask= mask)

		# print the shape of the image
		print(self.res.shape)

		# Convert the mask image to grayscale
		self.gray = cv2.cvtColor(self.res,cv2.COLOR_BGR2GRAY)
		# Convert the image to threshold image
		ret,self.threshold_im = cv2.threshold(self.gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

		# Find countours
		#im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		# Check for all connected components
		ret, labels, stats, centroids = cv2.connectedComponentsWithStats(self.threshold_im)
		label_hue = np.uint8(179*labels/np.max(labels))
		blank_ch = 255*np.ones_like(label_hue)
		labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

		labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
		labeled_img[label_hue==0] = 0


		# Some printing for debugging (can be removed later)
		print(stats.shape)

		# Sort the array accoring to the area of the connected components
		#reshuffled = sorted(stats[:], key = lambda x: x[:,4])
		reshuffled = stats[stats[:,4].argsort(),:]
		print(reshuffled)
		print(reshuffled.shape)

		# The largest blob is the background itset, so consider the second largest blob and draw a rectangle over it
		plate_coordinates = reshuffled[-2][:4]
		print(plate_coordinates)

		x,y,w,h = plate_coordinates[0], plate_coordinates[1], plate_coordinates[2],plate_coordinates[3]
		cv2.rectangle(self.frame, (x,y),(x+w,y+h),(0,0,255),5)

		return self.res,self.threshold_im, labeled_img, self.frame

img = cv2.imread(sys.argv[1])
object = Findextrema(img)
hsv_image, th_image, conn, detected = object.findextremepoints()

cv2.imshow("normal", img)
cv2.imshow("hsv", hsv_image)
cv2.imshow("thresholded", th_image)
cv2.imshow("connected", conn)
cv2.imshow("plate", detected)
cv2.waitKey(0)
cv2.destroyAllWindows()