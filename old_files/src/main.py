import sys
import os
sys.path.append("../")
#from communication import server
#from communication.publisher import Publish
import configparser
import eventModule as events
import inputModule 
import imageprocessingModule 
import json

PATH = os.getcwd()

def find_config_file(PATH):
	for _,_,file in os.walk(PATH):
		for f in file:
			if f.endswith(".ini"):
				configfile = f
	return PATH+"/"+configfile


if __name__ == '__main__':
	roi = []
	file_ = find_config_file(PATH)
	print("[INFO]: Found an ini file {}".format(file_))
	config = configparser.ConfigParser()
	config.read(file_)
	
	try:
		id_ = config['id']
		print("[INFO] Config file available")
	except:
		print("[INFO] Send Query to the master since there is no config")
	

	# start a worker to check for events and keep checking
	# parse list of ROIs in events
	init_input = inputModule.VideoHandler()

	print("[INFO] Video capture initialized")

	# convert the roi into list of lists
	print(len(config['roi']))
	for i in range(len(config['roi'])):
		print(config['roi'][str(i+1)][0])
		roi.append(json.loads(config['roi'][str(i+1)]))
	print("[INFO] The ROIs are {}".format(roi))
	event = events(roi)	

	
	while(True):
		color_frame = init_input.get_current_frame()
		event_log = event._motiontrigger(color_frame)
		if len(event_log) == 0:
			print("[INFO] No event detected")
		else:
			print("[ALERT] Event detected")
			# Publish to the master
