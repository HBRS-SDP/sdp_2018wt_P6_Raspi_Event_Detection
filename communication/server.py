import zmq
import time
import configparser

config = configparser.ConfigParser() 
config.read('distribute.ini')

port = config["ports"]["parent"]

# make the context
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

while True:
	msg = "this is under prod"
    socket.send(msg)
    msg = socket.recv()
    print msg
    time.sleep(1)