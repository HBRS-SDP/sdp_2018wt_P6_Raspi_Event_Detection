import zmq
import random
import sys
import time
import json

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

#while True:

def queryConfig(data):
    socket.send(json.dumps(data))
    msg = socket.recv()
    print msg
    

def publishEvent(data):
    socket.send(json.dumps(data))
    msg = socket.recv()
    print msg

if __name__=="__main__":

    queryConfig([1, "Query"])
    publishEvent("motion")
