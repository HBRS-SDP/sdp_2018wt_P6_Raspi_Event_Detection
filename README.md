# Raspberry Pi Event Detection

This project deals with detecting events in the scene using multiple raspberry Pis. The general setup, backend processes and "how-to" is described in this readme. Please note that there will not be any requirements file for this project since the setup process for a raspberry Pi is much different than that on a PC.


## Defining an event

The initial thought of event definition was quiet unclear since object motion is an event and so is object removal. However to narrow things down we define two major types of events:
1. Binary Events
	* Object Removal
	* Object Introduction

2. Sequential Events
	* Robot Arrival
	* Robot Departure
	* Object pick
	* Object place

Any of the aforementioend event has got one common trigger: The motion trigger. Whenever we have a motion (major noise in a binary frame) we spawn the events realted to motion trigger. Most of them are included within the scope of the motion trigger. However we can add more triggers as the project evolves.

## Modules and organization of the code
```
├── comm.txt
├── communication
│   ├── __init__.py
│   ├── master.py
│   └── slave.py
├── events
│   ├── conf.json
│   ├── cv.py
│   ├── __init__.py
│   ├── key.mp4
│   ├── myfile.xls
│   ├── object_motion.py
│   ├── object_removal.py
│   └── sample1.mp4
├── __init__.py
├── object_detection_module
│   ├── ball_on_table.jpg
│   └── find_white_plate.py
├── organization.txt
├── README.md
└── src
    ├── config.ini
    ├── eventModule.py
    ├── eventModule.pyc
    ├── imageprocessingModule.py
    ├── imageprocessingModule.pyc
    ├── __init__.py
    ├── inputModule.py
    ├── inputModule.pyc
    └── main.py
```

The project has three main modules and one experimental module. The core modules are:
	* communication
	* events
	* src

And the experimental module is:
	* object detection


