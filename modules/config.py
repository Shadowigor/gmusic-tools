#!/usr/bin/env python2

import sys
import os.path
from gmusicapi import Musicmanager
from misc import *

conf_path  = "data/config"
std_usr    = ""
root_dir   = "~"
trash_path = "~/.trash"
cred_path  = "data/credentials"
list_path  = "data/list"

def gmtConfigRead():
	global std_usr, root_path, trash_path, cred_path, list_path
	
	try:
		with open(conf_path, "r") as file:
			for line in file:
				
				if(line[:17] == "StandardUsername="):
					std_usr = line[17:-1]
					gmtDebug("StandardUser Config: " + std_usr)
					
				elif(line[:15] == "RootDirectiory="):
					root_dir = line[15:-1]
					gmtDebug("RootDirectory Config: " + root_dir)
					if not os.path.exists(root_dir):
						gmtError("Error: Song directory not found")
						return -2

				elif(line[:10] == "TrashPath="):
					trash_path = line[10:-1]
					gmtDebug("TrashPath Config: " + trash_path)
					if not os.path.exists(trash_path):
						if gmtAskUser("Couldn't find trash directory. Generate empty one now (y/n)? ") == "y":
							try:
								os.makedirs(trash_path)
							except IOError:
								gmtError("Couldn't generate trash directory")
								return -3
							break
						else:
							gmtError("Trash directory needed")
							return -4
					
				elif(line[:16] == "CredentialsPath="):
					cred_path = line[16:-1]
					gmtDebug("CredentialsPath Config: " + cred_path)
					if not os.path.isfile(cred_path):
						if gmtAskUser("Couldn't find credentials. Generate them now (y/n)? ") == "y":
							try:
								Musicmanager.perform_oauth(cred_path)
							except:
								gmtError("Generating credentials failed")
								return -5
						else:
							gmtError("Credentials needed")
							return -6
				
				elif(line[:17] == "UploadedListPath="):
					list_path = line[17:-1]
					gmtDebug("UploadedListPath Config: " + list_path)
					if not os.path.isfile(list_path):
						if gmtAskUser("Couldn't find list of uploaded files. Generate empty one now (y/n)? ") == "y":
							try:
								file = open(list_path, "w")
								file.close()
							except IOError:
								gmtError("Couldn't generate list of uploaded files")
								return -7
						else:
							gmtError("List of uploaded files needed")
							return -8
	except IOError:
		gmtError("Couldn't open config file")
		return -1
	return 0

def gmtConfigWrite(key, value):
	try:
		with open(conf_path, "r") as file:
			content = file.readlines()
		gmtDebug("gmtConfigWrite: Config file has " + str(len(content)) + " lines")
		
		for i in range(len(content)):
			if(content[i][:len(key)] == key):
				content[i] = key + "=" + value + "\n"
				with open(conf_path, "w") as file:
					file.writelines(content)
				return 0
		else:
			gmtDebug("gmtConfigWrite: Key not found, generating one")
			content.append(key + value)
			with open(conf_path, "w") as file:
				file.writelines(content)
			return 1
	except IOError:
		gmtError("Couldn't write config file")
		return -1
