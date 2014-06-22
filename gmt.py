
import modules.error as error
from modules.config import *
from modules.misc import *
from modules.duplicates import *
from modules.not_listened import *
from modules.sync import *
from modules.playlists import *
from modules.error import ERROR

gmtPrint("Reading Config... ", 0)
gmtConfigRead()
if ERROR:
    gmtError("Bad config")
gmtPrint("Done")

username, password = gmtGetLogin()

gmtPrint("Logging in... ", 0)
obj = gmtLogin(username, password)
if ERROR:
    gmtFatal("Couldn't Login")
gmtPrint("Done")

gmtPrint("Getting songs from Google Music... ", 0)
tracks = gmtGetAllSongs(obj)
if ERROR:
    gmtFatal("Couldn't get songs from google music")
gmtPrint("Done")

gmtPrint("Reading list of already uploaded songs... ")
list = gmtGetUploadedList()
if ERROR:
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
    gmtPrint(" ( 1) Synchronize Google Music and your local files")
    gmtPrint(" ( 2) Detect and delete duplicated tracks in Google Music")
    gmtPrint(" ( 3) Generate a playlist with tracks you haven't listened yet")
    gmtPrint(" ( 4) Insert album arts")
    gmtPrint(" ( 5) Backup metadata")
    gmtPrint(" ( 6) Reupload all songs")
    gmtPrint(" ( 7) Update list of uploaded files")
    gmtPrint(" ( 8) Change the music folder (currently " + modules.config.root_dir + ")")
    gmtPrint(" ( 9) Change trash directory")
    gmtPrint(" (10) Change path to credentials")
    gmtPrint(" (11) Change path to list of uploaded files")
    gmtPrint("")
    choice = gmtAskUser("Your choice: ", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
    
    if choice == "1":
        
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
                gmtUploadSongs(to_upload)
            
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
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        pass
    elif choice == "7":
        
        try:
            with open(modules.config.list_path, "w") as file:
                for x in tracks:
                    file.write(x["artist"] + "\t" + x["title"] + "\t" + x["album"] + "\n")
            gmt("Written list of uploaded files")
        except IOError:
            gmtError("Couldn't write list file")
        
    elif choice == "8":
        pass
    elif choice == "9":
        pass
    elif choice == "10":
        pass
    elif choice == "11":
        pass

gmtPrint("Logging out... ", 0)
gmtLogout(obj)
gmtPrint("Done")
