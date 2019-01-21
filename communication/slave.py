import zmq
import random
import sys
import time
import json

# port = "5556"
# context = zmq.Context()
# socket = context.socket(zmq.PAIR)
# socket.bind("tcp://*:%s" % port)

#while True:

class Slave:
	def __init__(self):
		self.port = "5556"
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.PAIR)
		self.socket.bind("tcp://*:%s" % self.port)


	def queryConfig(self, data):
		self.socket.send(json.dumps(data))
		msg = self.socket.recv()
		return msg
    

	def publishEvent(self,data):
		self.socket.send(json.dumps(data))
		msg = self.socket.recv()
		return msg

if __name__=="__main__":

	s = Slave()
	query = json.loads(s.queryConfig([1, "Query"]))
	if query:
		with open("conf.json", 'w') as f:
			json.dump(query,f)
	ack = s.publishEvent(json.dumps({'data': [['Object Introduced', ('2019/1/20', '18.6.13')]]}))
