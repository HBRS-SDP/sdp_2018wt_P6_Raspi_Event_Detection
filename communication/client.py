# just for reference, this will recide on the raspberry pis

import zmq
import random
import sys
import time
import configparser

config = configparser.ConfigParser() 
config.read('distribute.ini')

port = config["ports"]["default"]
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    msg = socket.recv()
    print msg
    socket.send("client message to server1")
    socket.send("client message to server2")
    time.sleep(1)