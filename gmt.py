
import sys
import pickle
import modules.error as error
import modules.config as config
from modules.config import *
from modules.misc import *
from modules.gmobject import *
from modules.duplicates import *
from modules.not_listened import *
from modules.sync import *
from modules.playlists import *
from modules.albumart import *

if "-v" in sys.argv:
    modules.misc.VERBOSE = 1
if "-vv" in sys.argv:
    modules.misc.VERBOSE = 2
if "-vvv" in sys.argv:
    modules.misc.VERBOSE = 3

gmtPrintV("Reading Config... ")
gmtConfigRead()
if error.e:
    gmtError("Bad config")
gmtPrintV("Done")

username, password = gmtGetLogin()

gmtPrint("Logging in... ", 0)
gmObj = gmObject()
gmObj.login(username, password)
if error.e:
    gmtFatal("Couldn't Login")
gmtPrint("Done")

gmtPrint("Getting songs from Google Music... ", 0)
tracks = gmtGetAllSongs(gmObj)
if error.e:
    gmtFatal("Couldn't get songs from google music")
gmtPrint("Done")

gmtPrint("Reading list of already uploaded songs... ")
list = gmtGetUploadedList()
if error.e:
    gmtFatal("Couldn't open list of already uploaded files")
gmtPrint("Done")

gmtPrint("")
gmtPrint("")
gmtPrint("Welcome to the gmusic-tools!")
gmtPrint("============================")
    
while 1:
    gmtPrint("")
    gmtPrint("Please select the action you would like to perform:")
    gmtPrint("")
    gmtPrint(" ( 0) Exit")
    gmtPrint(" ( 1) Synchronize Google Music and your local files")
    gmtPrint(" ( 2) Detect and delete duplicated tracks in Google Music")
    gmtPrint(" ( 3) Generate a playlist with tracks you haven't listened yet")
    gmtPrint(" ( 4) Insert album arts")
    gmtPrint(" ( 5) Backup metadata")
    gmtPrint(" ( 6) Reupload all songs")
    gmtPrint(" ( 7) Update list of uploaded files")
    gmtPrint(" ( 8) Change the music folder (currently " + config.root_dir + ")")
    gmtPrint(" ( 9) Change trash directory")
    gmtPrint(" (10) Change path to credentials")
    gmtPrint(" (11) Change path to list of uploaded files")
    gmtPrint("")
    choice = gmtAskUser("Your choice: ", ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
    
    if choice == "0":
        
        exit()
        
    elif choice == "1":
        
        to_upload, to_del_loc, to_del_rem = gmtGetSyncChanges(tracks, list)
        
        if to_upload == 1:
            gmtPrint("There are no changes to be made")
            continue
        
        if to_upload:
            gmtPrint("To Upload:")
            gmtPrint("")
            for x in to_upload:
                gmtPrint(x)
            gmtPrint("")
        
        if to_del_loc:
            gmtPrint("To Delete Locally:")
            gmtPrint("")
            for x in to_del_loc:
                gmtPrint(x)
            gmtPrint("")
        
        if to_del_rem:
            gmtPrint("To Delete Remotely:")
            gmtPrint("")
            for x in to_del_rem:
                gmtPrint(x["artist"] + " - " + x["title"] + " (" + x["album"] + ")")
            gmtPrint("")
        
        gmtPrint("")
        if gmtAskUser("Apply changes (y/n)? ") == "y":
            if to_upload:
                gmtUploadSongs(gmObj, to_upload)
            
            if to_del_loc:
                gmtPrint("Deleting local files... ", 0)
                gmtMoveToTrash(to_del_loc)
                gmtPrint("Done")
            
            if to_del_rem:
                gmtPrint("Deleting remote files... ", 0)
                gmtDeleteTracks(gmObj, to_del_rem)
                gmtPrint("Done")
        else:
            gmtPrint("Aborted")
        
    elif choice == "2":
        
        to_update, to_delete = gmtGetDuplicates(tracks)
        
        if len(to_update) == 0:
            gmtPrint("No duplicates found")
            continue
        
        gmtPrint("")
        gmtPrint("Duplicates:")
        gmtPrint("")
        for x in to_update:
            gmtPrint(x["artist"] + " - " + x["title"] + " (" + x["album"] + ")")
        gmtPrint("")
        if gmtAskUser("Apply changes (y/n)? ") == "y":
            gmtPrint("Updating tracks... ", 0)
            gmObj.change_song_metadata(to_update)
            gmtPrint("Done")
            gmtPrint("Deleting duplicates... ", 0)
            gmObj.delete_songs(to_delete)
            gmtPrint("Done")
        
    elif choice == "3":
        
        playlist = gmtGetNotListenedTracks(tracks)
        if len(playlist) == 0:
            gmtPrint("All tracks listened")
            continue
        name = gmtGetUserInput("Playlist name: ")
        gmtPrint("Generating Playlist... ", 0)
        gmtPlaylistNew(gmObj, playlist, name)
        gmtPrint("Done")
        
    elif choice == "4":
        
        to_update = []
        for i in range(len(tracks)):
            if tracks[i]["artist"] == u"Annakin" and tracks[i]["album"] == u"Stand Your Ground":
                tracks[i]["albumArtUrl"] = u"http://www.cede.ch/covers/cd/1131000/xl1131039.jpg" #gmtGetAlbumArtURL(tracks[i], "")
                to_update.append(tracks[i])
        gmObj.change_song_metadata(to_update)
        
    elif choice == "5":
        
        gmtPrint("Backing up Metadata... ", 0)
        try:
            with open("./data/meta.bk", "w") as file:
                pickle.dump(tracks, file, pickle.HIGHEST_PROTOCOL)
            gmtPrint("Done")
        except IOError:
            gmtPrint("Error while opening file")
        
    elif choice == "6":
        
        gmtPrint("Feature not implemented yet")
        
    elif choice == "7":
        
        try:
            with open(config.list_path, "w") as file:
                for x in tracks:
                    file.write(x["artist"] + "\t" + x["title"] + "\t" + x["album"] + "\n")
            gmt("Written list of uploaded files")
        except IOError:
            gmtError("Couldn't write list file")
        
    elif choice == "8":
        
        config.root_dir = gmtGetUserInput("New music directory: ");
        gmtPrint("Writing Config... ", 0)
        gmtConfigWrite("RootDirectory", config.root_dir)
        if error.e:
            gmtPrint("Error while writing config")
        else:
            gmtPrint("Done")
        
    elif choice == "9":
        
        config.trash_path = gmtGetUserInput("New trash directory: ");
        gmtPrint("Writing Config... ", 0)
        gmtConfigWrite("TrashPath", config.trash_path)
        if error.e:
            gmtPrint("Error while writing config")
        else:
            gmtPrint("Done")
        
    elif choice == "10":
        
        config.cred_path = gmtGetUserInput("New path to credentials: ");
        gmtPrint("Writing Config... ", 0)
        gmtConfigWrite("CredentialsPath", config.cred_path)
        if error.e:
            gmtPrint("Error while writing config")
        else:
            gmtPrint("Done")
        
    elif choice == "11":
        
        config.list_path = gmtGetUserInput("New path to list of uploaded files: ");
        gmtPrint("Writing Config... ", 0)
        gmtConfigWrite("UploadedListPath", config.list_path)
        if error.e:
            gmtPrint("Error while writing config")
        else:
            gmtPrint("Done")

gmtPrint("Logging out... ", 0)
gmtLogout(gmObj)
gmtPrint("Done")
