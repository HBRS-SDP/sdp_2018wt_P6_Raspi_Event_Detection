import sys
import os

PATH = os.getcwd()

def file_config_file(PATH):
	for _,_,file in os.walk(PATH):
		for f in file:
			if f.endswith(".ini"):
				configfile = f
	return PATH+"/"+configfile

