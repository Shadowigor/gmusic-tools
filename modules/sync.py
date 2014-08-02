#!/usr/bin/env python2

import os
import sys
import os.path
import modules.config
import modules.error as error
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from misc import *
from gmusicapi import Musicmanager

def gmtGetSyncChanges(tracks, list):
	error.e = 0
	
	to_upload = []
	to_delete = []
	list_out = ""
	i = 0
	last_i = 0
	
	gmtPrint("Synchronizing...   0%", 0)
	file_count = sum([len(files) for r, d, files in os.walk(modules.config.root_dir)])
	
	if(file_count == 0):
		gmtPrintV("No files found")
		error.e = error.NO_SONGS
		return [], [], []
	
	for root, subFolder, files in os.walk(modules.config.root_dir):
		for file in files:
			i += 1
	
			if((100 * i) / file_count > last_i):
				gmtPrint("\rSynchronizing... " + str((100 * i) / file_count).rjust(3) + "%", 0)
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
#					list_out = list_out + tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0] + "\n"
					tracks.remove(track)
					break
			else:
				if(tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0]).encode("utf8") in list:
					to_delete.append(file)
				else:
					to_upload.append(file)
#					upl_list_out.append(tag["artist"][0] + "\t" + tag["title"][0] + "\t" + tag["album"][0] + "\n")
	
	gmtPrint("\rSynchronizing... 100%")
	gmtPrintVV("gmtGetSyncChanges: To Upload: " + str(len(to_upload)) + " To Delete Locally: " + str(len(to_delete)) + " To Delete Remotely: " + str(len(tracks)))
	
	return to_upload, to_delete, tracks # To Upload, To Delete Locally, To Delete Remotely

def gmtMoveToTrash(to_delete):
	error.e = 0
	
	try:
		for x in to_delete:
			shutil.move(x, conf_trash_path)
		gmtPrintVV("gmtMoveToTrash: Moved " + str(len(to_delete)) + " files")
	except:
		gmtPrintV("gmtMoveToTrash: Cannot move files")
		error.e = error.FILE_ERROR

def gmtDeleteTracks(gmObj, to_delete):
	error.e = 0
	
	i = 0
	for x in to_delete:
		if not gmObj.mc.delete_songs(x["id"]):
			i += 1
	gmtPrintVV("gmtDeleteTracks: Deleted " + str(len(to_delete) - i) + " files")
	if i:
		gmtPrintV("Failed to delete " + str(i) + " songs")
		error.e = error.FILE_ERROR
		return -i
	return 0

def gmtUploadSongs(gmObj, to_upload):
	error.e = 0
	
	failed = []
	
	i = 0
	file_count = len(to_upload)
	gmtPrintVV("gmtUploadSongs: Files to upload: " + str(file_count))
	gmtPrint("Uploading files...   0% ", 0)
	for file in to_upload:
		gmtPrint("\33[2K\r", 0)
		gmtPrint("Uploading files... " + str((100 * i) / file_count).rjust(3) + "% " + file, 0)
		i += 1
		x = gmObj.mm.upload(file, "320k")
		if x[2]:
			failed.append(file)
	
	sys.stdout.write("\33[2K\r")
	gmtPrint("Uploading files... 100%")
	
	if failed:
		gmtPrintV("gmtUploadSongs: Failed to upload the following files:")
		for x in failed:
			gmtPrintV(x)
	
	return failed
