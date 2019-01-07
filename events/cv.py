import cv2
import sys, os
import json
import imutils
import numpy as np

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
normal = {}
normal["status"] = True
normal["prev"] = True
normal["count"] = 0

def locate_dice(frame, color):
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
	edges = cv2.Canny(frame, 100, 200)
	cv2.imshow("edge", edges)
	for i in range(2):
		edges = cv2.dilate(edges, kernel)
	cv2.imshow("dialated", edges)
	im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	try: hierarchy = hierarchy[0]
	except: hierarchy = []

	for c in contours:
		(x,y,w,h) = cv2.boundingRect(c)
		#min_x, max_x = min(x, min_x), max(x+w, max_x)
		#min_y, max_y = min(y, min_y), max(y+h, max_y)
		if 10 < h < 90 and 10 < w < 90:
			cv2.rectangle(color, (x,y), (x+w,y+h), (255, 0, 0), 2)
	#if max_x - min_x > 0 and max_y - min_y > 0:
	#	cv2.rectangle(color, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
	cv2.imshow("final", color)
	cv2.waitKey(7000)


while(True):
	ret, frame = cap.read()
	#print(ret)
	frame = cv2.resize(frame, (640,480))
	gray_ = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray_, (21, 21), 0)
	text = "Normal"
	normal["prev"] = True

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

		normal["prev"] = False
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Object Motion"

	if normal["prev"] == True:
		normal["count"] += 1
		if normal["count"] >= 25:
			print("NORMAL: {}".format(normal["count"]))
			locate_dice(gray_, frame)
			break

	cv2.putText(frame, "Table Status: {}".format(text), (10, 20),\
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	if conf["show_video"] == True:
		cv2.imshow("frames", frame)

	if cv2.waitKey(10) & 0xff==ord('q'):
		break

	#print("NROMAL+PRO: {}".format(normal["prev"]))

cv2.destroyAllWindows()
cap.release()