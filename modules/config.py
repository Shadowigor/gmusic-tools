#!/usr/bin/env python2

import sys
import os.path
import modules.error as error
from gmusicapi import Musicmanager
from misc import *
from modules.error import ERROR

conf_path  = "data/config"
std_usr    = ""
root_dir   = "~"
trash_path = "~/.trash"
cred_path  = "data/credentials"
list_path  = "data/list"

def gmtConfigRead():
	global std_usr, root_dir, trash_path, cred_path, list_path
	
	try:
		with open(conf_path, "r") as file:
			for line in file:
				
				if(line[:17] == "StandardUsername="):
					std_usr = line[17:-1]
					gmtPrintV("gmtConfigRead: StandardUser Config: " + std_usr)
					
				elif(line[:14] == "RootDirectory="):
					root_dir = line[14:-1]
					gmtPrintV("gmtConfigRead: RootDirectory Config: " + root_dir)
					if not os.path.exists(root_dir):
						gmtPrintV("gmtConfigRead: Song directory not found")
						ERROR = error.ROOT_DIR_NOT_FOUND
						return

				elif(line[:10] == "TrashPath="):
					trash_path = line[10:-1]
					gmtPrintV("gmtConfigRead: TrashPath Config: " + trash_path)
					if not os.path.exists(trash_path):
						gmtPrintV("gmtConfigRead: Couldn't find trash directory, generating empty one now")
						try:
							os.makedirs(trash_path)
						except IOError:
							gmtPrintV("gmtConfigReadCouldn't generate trash directory")
							ERROR = error.TRASH_ERROR
							return
				
				elif(line[:16] == "CredentialsPath="):
					cred_path = line[16:-1]
					gmtPrintV("gmtConfigRead: CredentialsPath Config: " + cred_path)
					if not os.path.isfile(cred_path):
						if gmtAskUser("Couldn't find credentials. Generate them now (y/n)? ") == "y":
							try:
								Musicmanager.perform_oauth(cred_path)
							except:
								gmtPrintV("gmtConfigRead: Generating credentials failed")
								ERROR = error.FILE_ERROR
						else:
							gmtPrintV("gmtConfigRead: Credentials needed to upload songs")
							ERROR = error.LOGIN_FAILED
				
				elif(line[:17] == "UploadedListPath="):
					list_path = line[17:-1]
					gmtPrintV("gmtConfigRead: UploadedListPath Config: " + list_path)
					if not os.path.isfile(list_path):
						gmtPrintV("gmtConfigRead: Couldn't find list of uploaded files, generating empty one now")
						try:
							file = open(list_path, "w")
							file.close()
						except IOError:
							gmtError("gmtConfigRead: Couldn't generate list of uploaded files")
							ERROR = error.LIST_ERROR
							return
	except IOError:
		gmtPrintV("gmtConfigRead: Couldn't open config file")
		ERROR = error.CONFIG_READ_ERROR
		return

def gmtConfigWrite(key, value):
	try:
		with open(conf_path, "r") as file:
			content = file.readlines()
		gmtPrintVV("gmtConfigWrite: Config file has " + str(len(content)) + " lines")
		
		for i in range(len(content)):
			if(content[i][:len(key)] == key):
				content[i] = key + "=" + value + "\n"
				with open(conf_path, "w") as file:
					file.writelines(content)
				return 0
		else:
			gmtPrintV("gmtConfigWrite: Key not found, generating one")
			content.append(key + value)
			with open(conf_path, "w") as file:
				file.writelines(content)
	except IOError:
		gmtPrintV("Couldn't write config file")
		ERROR = error.CONFIG_WRITE_FAILED
