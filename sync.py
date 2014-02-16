#!/usr/bin/env python

from gmusicapi import Mobileclient, Musicmanager
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
import shutil
import os
import sys
import getpass
import os.path

### DEFINED BY THE USER ########################################################

# Here is where the music is stored
rootdir = "/data/Musik/01/"

# Songs won't be automatically deleted, they will be moved to that location instead
trash = "./.trash/"

# Here is a list of the already uploaded files
list_path = "./list"

# Credentials file for the Musicmanager
cred_path = "./credentials"

################################################################################

# Check the user-defined file paths
if not os.path.exists(rootdir):
	print "Error: Song directory not found"
	exit()

if not os.path.exists(trash):
	while 1:
		sys.stdout.write("Couldn't find trash directory. Generate empty one now (y/n)? ")
		sys.stdout.flush()
		x = sys.stdin.readline()
		if(x == "y\n"):
			try:
				os.makedirs(trash)
			except IOError:
				print "Error: Couldn't generate trash directory"
				exit()
			break
		elif(x == "n\n"):
			print "Error: Trash directory needed"
			exit()

if not os.path.isfile(list_path):
	while 1:
		sys.stdout.write("Couldn't find list of uploaded files. Generate empty one now (y/n)? ")
		sys.stdout.flush()
		x = sys.stdin.readline()
		if(x == "y\n"):
			try:
				file = open(list_path, "w")
				file.close()
			except IOError:
				print "Error: Couldn't generate list of uploaded files"
				exit()
			break
		elif(x == "n\n"):
			print "Error: List of uploaded files needed"
			exit()

if not os.path.isfile(cred_path):
	while 1:
		sys.stdout.write("Couldn't find credentials. Generate them now (y/n)?")
		sys.stdout.flush()
		x = sys.stdin.readline()
		if(x == "y\n"):
			Musicmanager.perform_oauth(cred_path)
			break
		elif(x == "n\n"):
			print "Error: Credentials needed"
			exit()

# Get username and password
sys.stdout.write("Username: ")
sys.stdout.flush()
username = sys.stdin.readline()[:-1]

password = getpass.getpass()

# Login into Google Music
sys.stdout.write("Logging in... ")
sys.stdout.flush()
gm_mc = Mobileclient()
if not gm_mc.login(username, password):
	print "Error: Wrong username or password (or no internet connection)"
	exit()
print "Done"

#Get all songs from Google Music
sys.stdout.write("Getting songs from Google Music... ")
sys.stdout.flush()
tracks = gm_mc.get_all_songs()
if not tracks:
	print "Error: No tracks found"
	gm_mc.logout()
	exit()
print "Done"

# Get list of already uploaded songs
sys.stdout.write("Reading file of uploaded songs... ")
sys.stdout.flush()
try:
	with open(list_path, "r+") as list_file:
		list = list_file.read().split('\n')
except IOError:
	print "Error: Couldn't open list of uploaded files (What have you done to it?!)"
	gm_mc.logout()
	exit()
print "Done"

to_upload = []
to_delete = []
failed = []
upl_list_out = []
list_out = ""
i = 0
last_i = 0

sys.stdout.write("\rSynchronising...   0%")
sys.stdout.flush()
file_count = sum([len(files) for r, d, files in os.walk(rootdir)])

if(file_count == 0):
	print "Error: No files found"
	gm_mc.logout()
	exit()

# Check what we have to upload or delete
for root, subFolder, files in os.walk(rootdir):
	for file in files:
		i += 1

		if((100 * i) / file_count > last_i):
			sys.stdout.write("\rSynchronising... " + str((100 * i) / file_count).rjust(3) + "%")
			sys.stdout.flush()
			last_i += 1

		file = root + '/' + file
		if file[-4:] == ".mp3":
			tag = EasyID3(file)
		elif file[-5:] == ".flac":
			tag = FLAC(file)
		else:
			continue

		for track in tracks:
			if(
			  track["artist"] == tag["artist"][0] and
			  track["title"]  == tag["title"][0] and
			  track["album"]  == tag["album"][0]):
				list_out = list_out + tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0] + "\n"
				tracks.remove(track)
				break
		else:
			if(tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0]).encode("utf8") in list:
				to_delete.append(file)
			else:
				to_upload.append(file)
				upl_list_out.append(tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0] + "\n")

# Check if there is something to change
if not to_upload and not to_delete and not tracks:
	print "\nThere are no changes to be made"
	gm_mc.logout()
	exit()

# Print the changes to will be made
print "\n\nTo upload:\n"
for x in to_upload:
	print x

print "\nTo delete locally:\n"
for x in to_delete:
	print x

print "\nTo delete remotely:\n"
for x in tracks:
	print x["artist"] + "\t" + x["title"] + "\t" + x["album"]
sys.stdout.write("\n")

# Ask the user what to do next
while 1:
	sys.stdout.write("Execute changes (y/n)? ")
	sys.stdout.flush()
	x = sys.stdin.readline()
	if(x == "y\n"):
		break
	elif(x == "n\n"):
		gm_mc.logout()
		exit()

# Delete the local files that were deleted in Google Music
if to_delete:
	sys.stdout.write("Deleting local files... ")
	sys.stdout.flush()
	try:
		for t in to_delete:
			shutil.move(t, trash)
	except:
		print "Error: Cannot move files"
		gm_mc.logout()
		exit()
	print "Done"

# Delete the tracks in Google Music that were deleted locally
i = 0
if tracks:
	sys.stdout.write("Deleting remote files... ")
	for t in tracks:
		if not gm_mc.delete_songs(t["id"]):
			i += 1
	print "Done"
if i:
	print "Failed to delete " + i + " songs"

gm_mc.logout()

if to_upload:
	sys.stdout.write("Logging in... ")
	sys.stdout.flush()
	gm_mm = Musicmanager()
	if not gm_mm.login(cred_path):
		print "Error: Wrong credentials"
		exit()
	print "Done"

	# Upload the files that were not already in Google Music
	sys.stdout.write("Uploading files...   0% ")
	sys.stdout.flush()
	i = 0
	file_count = len(to_upload)
	for file in to_upload:
		sys.stdout.write("\33[2K\r")
		sys.stdout.write("Uploading files... " + str((100 * i) / file_count).rjust(3) + "% " + file)
		sys.stdout.flush()
		i += 1
		x = gm_mm.upload(file)
		if x[2]:
			failed.append(file)
		else:
			list_out = list_out + upl_list_out.pop(0)

	gm_mm.logout()
	sys.stdout.write("\33[2K\r")
	print "Uploading files... 100%"

	if failed:
		print "\nFailed to Upload the following files:\n"
		for x in failed:
			print x

sys.stdout.write("Writing list file of uploaded files... ")
sys.stdout.flush()
try:
	with open(list_path, "w") as list_file:
		list_file.write(list_out.encode("utf8"))
except IOError:
	print "Error: Cannot write list of uploaded files"
	exit()
print "Done"
