#!/usr/bin/env python2

import sys
import os.path
from gmusicapi import Mobileclient
from operator import itemgetter
from getpass import getpass
import modules.config

DEBUG = 1

def gmtGetAllSongs(gmObj):
	if not isinstance(gmObj, Mobileclient):
		gmtDebug("gmtGetAllSongs: Argument is not a valid GM-Object")
		return -1
	
	tracks = gmObj.get_all_songs()
	if not tracks:
		gmtError("Couldn't get tracks from Google Music")
		return -2
	gmtDebug("gmtGetAllSongs: Got list of " + str(len(tracks)) + " Tracks")
	
	tracks = sorted(tracks, key=itemgetter("artist", "album", "title"))
	return tracks

def gmtGetLogin():
	if modules.config.std_usr != "":
		gmtPrint("Using standard user, leave password blank to change")
		gmtPrint("Username: " + modules.config.std_usr)
	username = modules.config.std_usr
	password = ""
	while password == "":
		if username == "":
			username = gmtGetUserInput("Username: ")
			if gmtAskUser("Save username as standard username (y/n)? ") == "y" :
				if  modules.config.gmtConfigWrite("StandardUsername", username) < 0:
					gmtError("Couldn't write config for standard user")

		password = getpass()
		if password == "":
			username = ""

	return username, password

def gmtLogin(username, password):
	gmObj = Mobileclient()
	if not gmObj.login(username, password):
		gmtError("Wrong username or password (or no internet connection)")
		return -1

	return gmObj

def gmtLogout(gmObj):
	if isinstance(gmObj, Mobileclient):
		gmObj.logout()

def gmtGetUploadedList():
	try:
		if os.path.isfile(modules.config.list_path):
			with open(modules.config.list_path, "r") as file:
				list = file.read().split('\n')
			gmtDebug("Read list of " + str(len(list)) + " track")
		else:
			open(modules.config.list_path, "w").close()
			gmtDebug("gmtGetUploadedList: List doesn't exist, generating new one")
			return []
	except IOError:
		gmtError("Couldn't open list of uploaded files")
		return -1

	return list

def gmtAskUser(message, answers = ["y", "n"]):
	while 1:
		sys.stdout.write(message)
		sys.stdout.flush()
		x = sys.stdin.readline()
		for answer in answers:
			if(x == answer + "\n"):
				return answer

def gmtGetUserInput(message = ""):
	gmtPrint(message, 0)
	return sys.stdin.readline()[:-1]

def gmtDebug(message):
	if(DEBUG):
		print "[DEBUG] " + message

def gmtPrint(message, newline = 1):
	if(newline):
		print message
	else:
		sys.stdout.write(message)
		sys.stdout.flush()

def gmtError(message):
	sys.stderr.write("[ERROR] " + message + "\n")

def gmtFatal(message):
	sys.stderr.write("[FATAL] " + message + "\n")
	exit()
