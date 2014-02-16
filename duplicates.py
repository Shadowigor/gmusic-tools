#!/usr/bin/env python

from operator import itemgetter
from gmusicapi import Mobileclient
import sys
import getpass

# Get username and password
sys.stdout.write("Username: ")
sys.stdout.flush()
username = sys.stdin.readline()[:-1]

password = getpass.getpass()

# Login into Google Music
sys.stdout.write("Logging in... ")
sys.stdout.flush()
session = Mobileclient()
if(not session.login(username, password)):
	print "Error: Wrong username or password (or no internet connection)"
	exit()
print "Done"

to_delete = []
to_update = []

# Get all songs from Google Music
sys.stdout.write("Getting songs from Google Music... ")
sys.stdout.flush()
tracks = session.get_all_songs()
if(not tracks):
	print "Error while getting list of tracks"
	exit()
tracks = sorted(tracks, key=itemgetter("artist", "album", "title"))
print "Done"

i = 0
last_i = 0

while(i < len(tracks) - 2):
	if((100 * i) / len(tracks) > last_i):
		sys.stdout.write("\rSynchronising... " + str((100 * i) / len(tracks)).rjust(3) + "%")
		sys.stdout.flush()
		last_i += 1
	while(
	  tracks[i]["artist"] == tracks[i + 1]["artist"] and
	  tracks[i]["title"]  == tracks[i + 1]["title"] and
	  tracks[i]["album"]  == tracks[i + 1]["album"]):
		if(tracks[i]["creationTimestamp"] > tracks[i + 1]["creationTimestamp"]):
			x = i + 1
		else:
			x = i
		play_count = tracks[x]["playCount"]
		rating = tracks[x]["rating"]
		to_delete.append(tracks[x]["id"])
		del tracks[x]
		tracks[i]["playCount"] = play_count
		tracks[i]["rating"] = rating
		to_update.append(tracks[i])
	i += 1;
print "\rSynchronising... 100%"

if not to_update:
	print "There are no changes to be made"
	session.logout()
	exit()

# Print the changes
print "\nDuplicates:\n"
for x in to_update:
	print x["artist"] + " - " + x["title"] + " (" + x["album"] + ")"

# Ask the user what to do next
while 1:
	sys.stdout.write("\nExecute " + str(len(to_update)) + " changes (y/n)? ")
	sys.stdout.flush()
	x = sys.stdin.readline()
	if(x == "y\n"):
		break
	elif(x == "n\n"):
		session.logout()
		exit()

# Update song metadata
sys.stdout.write("Changing song metadata... ")
sys.stdout.flush()
session.change_song_metadata(to_update)
print "Done"
sys.stdout.write("Deleting duplicates... ")
sys.stdout.flush()
session.delete_songs(to_delete)
session.logout()
print "Done"
