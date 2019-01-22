import zmq
import random
import sys
import time
import json 

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

config = [{"id":1, "data": {"id":1, "roi":[[[199,42],[604,315]]], "events":["grasp","release", "object_removal"], "fps":7}}, {"id":2, "data": {"id":1, "roi":[[[199,42],[604,315]]]}}]
print(len(config))
all_data = []
while True:
    msg = json.loads(socket.recv())
    print msg
    #socket.send("client message to server1")
    #socket.send("client message to server2")
    print(len(config))
    if "Query" in msg:# == [1,"Query"]:
	for i in range(len(config)):
		if config[i]["id"] == msg[0]:
			print("I am here")
			#socket.send_json(config[i]["data"], flags|zmq.SNDMORE)
			socket.send(json.dumps(config[i]["data"]))

    elif "data" in msg:
	all_data.append(json.loads(msg))
	socket.send("OK")
    time.sleep(1)
