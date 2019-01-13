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

