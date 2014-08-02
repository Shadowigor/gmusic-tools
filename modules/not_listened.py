#!/usr/bin/env python2

import sys
import modules.error as error
from modules.misc import *

def gmtGetNotListenedTracks(tracks):
	error.e = 0
	
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
			error.e = error.PLAYLIST_FULL
			break
	
	gmtPrint("\rProcessing songs... 100%")
	return playlist
