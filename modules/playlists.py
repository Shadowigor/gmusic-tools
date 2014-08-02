#!/usr/bin/env python2

def gmtPlaylistNew(gmObj, playlist, name):
	gmObj.mc.add_songs_to_playlist(gmObj.mc.create_playlist(name), playlist)
