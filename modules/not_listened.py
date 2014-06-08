#!/usr/bin/env python2

import sys

def gmtGetNotListenedTracks(tracks):
	playlist = []
	i = 0
	
	# Get not yet listened tracks
	sys.stdout.write("Processing songs...   0%")
	sys.stdout.flush()
	for track in tracks:
		i += 1
		sys.stdout.write("\rProcessing songs... " + str((100 * i) / len(tracks)).rjust(3) + "%")
		sys.stdout.flush()
		if(track["playCount"] == 0):
			playlist.append(track["id"])
		if(len(playlist) >= 1000):
			print " Playlist full"
			break
	return playlist

# 	
# 	# Getting playlists
# 	sys.stdout.write("\nGetting playlists... ")
# 	sys.stdout.flush()
# 	playlists = api.get_all_playlists()
# 	print "Done"
# 	
# 	i = 1
# 	pl_id = 0
# 	while i:
# 		sys.stdout.write("Playlist name: ")
# 		sys.stdout.flush()
# 		pl_name = sys.stdin.readline()[:-1]
# 	
# 		for pl in playlists:
# 			if pl["name"] == pl_name:
# 				while 1:
# 					sys.stdout.write("Playlist already exists. Add the songs to it (y/n)?: ")
# 					sys.stdout.flush()
# 					x = sys.stdin.readline()
# 				        if(x == "y\n"):
# 				        	i = 0
# 				        	pl_id = pl["id"]
# 						break
# 					elif(x == "n\n"):
# 						break
# 				break
# 		else:
# 			break
# 	
# 	if not pl_id:
# 		# Creating playlist
# 		sys.stdout.write("Getting playlists... ")
# 		sys.stdout.flush()
# 		pl_id = api.create_playlist(pl_name)
# 		print "Done"
# 	
# 	# Shuffle playlist
# 	sys.stdout.write("Shuffling playlist... ")
# 	sys.stdout.flush()
# 	shuffle(playlist)
# 	print "Done"
# 	
# 	# Add songs to playlist
# 	sys.stdout.write("Adding songs to playlist... ")
# 	sys.stdout.flush()
# 	api.add_songs_to_playlist(pl_id, playlist)
# 	print "Done"
# 	
# 	api.logout()
