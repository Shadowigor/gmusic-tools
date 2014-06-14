#!/usr/bin/env python2

import sys

def gmtGetNotListenedTracks(tracks):
	playlist = []
	i = 0
	
	# Get not yet listened tracks
	gmtPrint("Processing songs...   0%", 0)
	for track in tracks:
		i += 1
		gmtPrint("\rProcessing songs... " + str((100 * i) / len(tracks)).rjust(3) + "%", 0)
		if(track["playCount"] == 0):
			playlist.append(track["id"])
		if(len(playlist) >= 1000):
			gmtPrint(" Playlist full")
			break
	return playlist
