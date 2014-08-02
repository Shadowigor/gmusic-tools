#!/usr/bin/env python2

import sys
import os.path
import modules.config
import modules.error as error
from gmusicapi import Mobileclient
from operator import itemgetter
from getpass import getpass

VERBOSE = 0

def gmtGetAllSongs(gmObj):
	error.e = 0
	
	if not isinstance(gmObj.mc, Mobileclient):
		error.e = error.INVALID_ARGUMENT
		gmtFatal("gmtGetAllSongs: Argument is not a valid GM-Object")
	
	tracks = gmObj.mc.get_all_songs()
	if not tracks:
		error.e = error.NO_SONGS
		gmtPrintV("gmtGetAllSongs: Couldn't get tracks from Google Music")
		return []
	gmtPrintVV("gmtGetAllSongs: Got list of " + str(len(tracks)) + " Tracks")
	
	tracks = sorted(tracks, key=itemgetter("artist", "album", "title"))
	
	return tracks

def gmtGetLogin():
	error.e = 0
	
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
					error.e = error.CONFIG_WRITE_FAILED

		password = getpass()
		if password == "":
			gmtPrintVVV("Password blank, changing username")
			username = ""

	return username, password

def gmtGetUploadedList():
	error.e = 0
	
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
		error.e = error.FILE_ERROR

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
