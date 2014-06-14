#!/usr/bin/env python2

def gmtPlaylistNew(gmObj, playlist, name):
	gmObj.add_songs_to_playlist(gmObj.create_playlist(name), playlist)
