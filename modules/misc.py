#!/usr/bin/env python2

from gmusicapi import Mobileclient
from operator import itemgetter
import sys
import getpass
import getpass
import os.path

# Get all songs from Google Music and sort them
def gmtGetAllSongs(gmObj):
	if not isinstance(gmObj, Mobileclient):
		return -1
	
	sys.stdout.write("Getting songs from Google Music... ")
	sys.stdout.flush()
	tracks = gmObj.get_all_songs()
	if(not tracks):
		sys.stderr.write("Error while getting list of tracks\n")
		return -1
	
	tracks = sorted(tracks, key=itemgetter("artist", "album", "title"))
	print "Done"
	return tracks

# Gets the login credentials from the console
def gmtGetLogin():
	# Get standard username
	if os.path.isfile(std_usr_file):
		try:
			with open(std_usr_file, "r") as file:
				username = file.readline()
				print "Using standard user (" + username + ")"
				print "Leave password blank to change the username"
		except IOError:
			username = ""
	else:
		username = ""

	password = ""
	while password == "":
		# Get username
		if username == "":
			sys.stdout.write("Username: ")
			sys.stdout.flush()
			username = sys.stdin.readline()[:-1]
			x = ""
			while x != "n\n":
				sys.stdout.write("Save username as standard username (y/n)? ")
				sys.stdout.flush()
				x = sys.stdin.readline()
				if(x == "y\n" or x == "\n"):
					try:
						with open(std_usr_file, "w") as file:
							file.write(username)
					except IOError:
						sys.stderr.write("Error: Couldn't write standard user to file\n")
					break

		# Get password
		password = getpass.getpass()
		if password == "":
			username = ""
		
		return username, password

def gmtLogin(username, password):
	sys.stdout.write("Logging in... ")
	sys.stdout.flush()
	gmObj = Mobileclient()
	if not gmObj.login(username, password):
		sys.stderr.write("Error: Wrong username or password (or no internet connection)\n")
		return -1
	print "Done"
	return gmObj

def gmtGetUploadedList():
	sys.stdout.write("Reading file of uploaded songs... ")
	sys.stdout.flush()
	try:
		with open(conf_list_path, "r+") as file:
			list = file.read().split('\n')
	except IOError:
		print "Error: Couldn't open list of uploaded files (What have you done to it?!)"
		return -1
	print "Done"
	return list
