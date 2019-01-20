import zmq
import random
import sys
import time
import json 

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    msg = json.loads(socket.recv())
    print msg
    #socket.send("client message to server1")
    #socket.send("client message to server2")
    if msg == [1,"Query"]:
	socket.send("Send ROI details")
    elif msg == "motion":
	socket.send("OK")
    time.sleep(1)
