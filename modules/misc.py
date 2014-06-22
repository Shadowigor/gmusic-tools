#!/usr/bin/env python2

import sys
import os.path
import modules.config
import modules.error as error
from gmusicapi import Mobileclient
from operator import itemgetter
from getpass import getpass
from modules.error import ERROR

VERBOSE = 3

def gmtGetAllSongs(gmObj):
	ERROR = 0
	
	if not isinstance(gmObj, Mobileclient):
		ERROR = error.INVALID_ARGUMENT
		gmtFatal("gmtGetAllSongs: Argument is not a valid GM-Object")
	
	tracks = gmObj.get_all_songs()
	if not tracks:
		ERROR = error.NO_SONGS
		gmtPrintV("gmtGetAllSongs: Couldn't get tracks from Google Music")
		return []
	gmtPrintVV("gmtGetAllSongs: Got list of " + str(len(tracks)) + " Tracks")
	
	tracks = sorted(tracks, key=itemgetter("artist", "album", "title"))
	
	return tracks

def gmtGetLogin():
	ERROR = 0
	
	if modules.config.std_usr != "":
		gmtPrintV("Using standard user, leave password blank to change")
		gmtPrint("Username: " + modules.config.std_usr)
	username = modules.config.std_usr
	password = ""
	while password == "":
		if username == "":
			username = gmtGetUserInput("Username: ")
			if gmtAskUser("Save username as standard username (y/n)? ") == "y" :
				if  modules.config.gmtConfigWrite("StandardUsername", username) < 0:
					gmtPrintV("Couldn't write config for standard user")
					ERROR = error.CONFIG_WRITE_FAILED

		password = getpass()
		if password == "":
			gmtPrintVVV("Password blank, changing username")
			username = ""

	return username, password

def gmtLogin(username, password):
	ERROR = 0
	
	gmObj = Mobileclient()
	if not gmObj.login(username, password):
		gmtPrintV("Wrong username or password (or no internet connection)")
		ERROR = error.LOGIN_FAILED
		return 0

	return gmObj

def gmtLogout(gmObj):
	ERROR = 0
	
	if isinstance(gmObj, Mobileclient):
		gmObj.logout()
	else:
		gmtPrintVV("Tried to logout a non-GM-Object")
		ERROR = error.INVALID_ARGUMENT
	

def gmtGetUploadedList():
	ERROR = 0
	
	try:
		if os.path.isfile(modules.config.list_path):
			with open(modules.config.list_path, "r") as file:
				list = file.read().split('\n')
			gmtPrintV("gmtGetUploadedList: Read list of " + str(len(list)) + " tracks")
		else:
			open(modules.config.list_path, "w").close()
			gmtPrintV("gmtGetUploadedList: List doesn't exist, generating new one")
			return []
	except IOError:
		gmtPrintV("gmtGetUploadedList: Couldn't open list of uploaded files")
		ERROR = error.FILE_ERROR

	return list

def gmtAskUser(message, answers = ["y", "n"]):
	
	while 1:
		gmtPrint(message, 0)
		x = sys.stdin.readline()
		for answer in answers:
			if(x == answer + "\n"):
				return answer

def gmtGetUserInput(message = ""):
	gmtPrint(message, 0)
	return sys.stdin.readline()[:-1]

def gmtPrint(message, newline = 1):
	if(newline):
		print message
	else:
		sys.stdout.write(message)
		sys.stdout.flush()

def gmtPrintV(message):
	global VERBOSE
	
	if(VERBOSE >= 1):
		gmtPrint("[  V] " + message)

def gmtPrintVV(message):
	global VERBOSE
	
	if(VERBOSE >= 2):
		gmtPrint("[ VV] " + message)

def gmtPrintVVV(message):
	global VERBOSE
	
	if(VERBOSE >= 3):
		gmtPrint("[VVV] " + message)

def gmtFatal(message):
	sys.stderr.write("[FATAL] " + message + "\n")
	exit()
