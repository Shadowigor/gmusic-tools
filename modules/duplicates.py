#!/usr/bin/env python2

import sys
import modules.error as error
from misc import *

def gmtGetDuplicates(tracks):
	error.e = 0
	
	to_delete = []
	to_update = []
	i = 0
	last_i = 0
	
	while(i < len(tracks) - 2):
		if((100 * i) / len(tracks) > last_i):
			gmtPrint("\rSynchronizing... " + str((100 * i) / len(tracks)).rjust(3) + "%", 0)
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
	gmtPrint("\rSynchronizing... 100%")
	
	return to_update, to_delete
