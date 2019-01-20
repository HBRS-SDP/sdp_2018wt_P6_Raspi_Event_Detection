import sys
import os
sys.path.append("../")
from communication import slave
#from communication.publisher import Publish
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
	return PATH+"/"+configfile


if __name__ == '__main__':
	roi = []
	file_ = find_config_file(PATH)
	print("[INFO]: Found an ini file {}".format(file_))
	# config = configparser.ConfigParser()
	# config.read(file_)
	conf = json.load(open(file_))
	
	try:
		id_ = conf["id"]
		print("[INFO] Config file available")
	except:
		print("[INFO] Send Query to the master since there is no config")
		query = json.loads(s.queryConfig([1, "Query"]))
		if query:
			with open("conf.json", 'w') as f:
				json.dump(query,f)

	

	# start a worker to check for events and keep checking
	# parse list of ROIs in events
	init_input = inputModule.VideoHandler()
	print("[INFO] Video capture initialized")

	# convert the roi into list of lists
	print(len(conf["roi"]))
	# Conf roi is a list of lists as [[(x1,y1), (x2,y2)],[(x3,y3),(x4,y4)], [(),()]......]
	event = events.Event(roi)	

	
	while(True):
		color_frame = init_input.get_current_frame()
		if type(color_frame) == type(None):
			break
		#event_log = event._motiontrigger(color_frame)

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