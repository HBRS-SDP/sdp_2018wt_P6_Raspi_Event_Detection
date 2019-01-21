import sys
import os
sys.path.append("../")
from communication import slave
import configparser
import eventModule as events
import inputModule 
import imageprocessingModule 
import json

s = slave.Slave()
PATH = os.getcwd()

def find_config_file(PATH):
	for _,_,file in os.walk(PATH):
		for f in file:
			if f.endswith(".json"):
				configfile = f
				break
		configfile = "nothin"
				#return PATH+"/"+configfile
	if configfile.endswith(".json"):
		return PATH+"/"+configfile
	else:
		return 0


if __name__ == '__main__':

	"""
	-------------------------------------------------
	Main File
	-------------------------------------------------

	Usage: 1. python main.py video <videofile> [for using it video a video clip]
	       2. python main.py raspi [for using it with raspberry pi]
	       3. python main.py pc [for using it with laptop camera]
	"""

	try:
		n = sys.argv[1]
	except:
		print("Welcome to Raspberry Pi based Event detection. You can use this file in the following configuration: \n\
			----------------------------------------------------------------------------------------------------------\n\
			python main.py video <videofile> [for using it video a video clip]\n\
			python main.py raspi [for using it with raspberry pi] \n\
			python main.py pc [for using it with laptop camera] \n\
			----------------------------------------------------------------------------------------------------------")
		sys.exit(0)
	
	# Define a list #roi which appends the ROIs from the configuration file
	roi = []
	# Find the config file, if there is None, the function returns 0
	file_ = find_config_file(PATH)
	print("[INFO]: Found an json file {}".format(file_))
	
	if file_ != 0:
		# read the json file it there is one
		conf = json.load(open(file_))
	else:
		# Query to the master, save it as conf.json and read it 
		print("[INFO] Send Query to the master since there is no config")
		query = json.loads(s.queryConfig([1, "Query"]))
		if query:
			with open("conf.json", 'w') as f:
				json.dump(query,f)
		conf = json.load(open("conf.json"))
	

	# start a worker to check for events and keep checking
	# parse list of ROIs in events
	init_input = inputModule.VideoHandler()
	print("[INFO] Video capture initialized")

	# Conf roi is a list of lists as [[(x1,y1), (x2,y2)],[(x3,y3),(x4,y4)], [(),()]......]
	# parse all rois and events
	#event = events.Event(roi)
	event = events.Event(conf["roi"], conf["events"])

	
	while(True):

		# Fetch the frame
		color_frame = init_input.get_current_frame()
		if type(color_frame) == type(None):
			break

		# Check all rois individually for events
		for i in range(len(conf["roi"])):
				segment = color_frame[conf["roi"][i][0][1]:conf["roi"][i][1][1], \
				conf["roi"][i][0][0]:conf["roi"][i][1][0]]
				event_log = event.eventManager(color_frame, segment, conf["roi"][i])
				if len(event_log) == 0:
					print("[INFO] No event detected")
				else:
					print("[ALERT] Event detected")
					print(event_log)
					try:
						ack = s.publishEvent(json.dumps(event_log))
						if ack:
							print("[INFO]: EVENT LOGGED")
					except:
						print("[ERR]: Please check the communication module for error, run unittests within")
	
			# Publish to the master
print("[INFO]: Processing ended")
