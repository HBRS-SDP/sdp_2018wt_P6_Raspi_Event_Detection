import cv2
import sys, os
import json
import imutils

#-------------------------------------------------------------------#
"""
Sample event to notify if a single object is removed from the scene

Contributed by: Vishwas Sharma
"""
#--------------------------------------------------------------------#


conf = json.load(open("conf.json"))
print(conf["input"])
cap = cv2.VideoCapture(conf["input"])
print(cap)
avg = None

while(True):
	ret, frame = cap.read()
	#print(ret)
	frame = cv2.resize(frame, (640,480))
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	text = "Normal"

	# if the average frame is None, initialize it
	if avg is None:
		print("[INFO] starting background model...")
		avg = gray.copy().astype("float")
		continue
	cv2.accumulateWeighted(gray, avg, 0.7)
	frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

	thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	#cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	#cnts = imutils.grab_contours(cnts)
		# loop over the contours
	for c in contours:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < conf["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Object Motion"

	cv2.putText(frame, "Table Status: {}".format(text), (10, 20),\
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	if conf["show_video"] == True:
		cv2.imshow("frames", frame)

	if cv2.waitKey(10) & 0xff==ord('q'):
		break


cv2.destroyAllWindows()
cap.release()