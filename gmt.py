
from modules.config import *
from modules.misc import *
from modules.duplicates import *
from modules.not_listened import *
from modules.sync import *
from modules.playlists import *

gmtPrint("Reading Config... ", 0)
if gmtConfigRead() < 0:
    gmtFatal("Bad config")
gmtPrint("Done")

username, password = gmtGetLogin()

gmtPrint("Logging in... ", 0)
obj = gmtLogin(username, password)
if obj == -1:
    gmtFatal("Couldn't Login")
gmtPrint("Done")

gmtPrint("Getting songs from Google Music... ", 0)
tracks = gmtGetAllSongs(obj)
if tracks < 0:
    gmtFatal("Couldn't get songs from google music")
gmtPrint("Done")

gmtPrint("Reading list of already uploaded songs... ")
list = gmtGetUploadedList()
if list == -1:
    gmtFatal("Couldn't open list of already uploaded files")
gmtPrint("Done")

while 1:
    gmtPrint("")
    gmtPrint("")
    gmtPrint("Welcome to the gmusic-tools!")
    gmtPrint("============================")
    gmtPrint("")
    gmtPrint("Please select the action you would like to perform:")
    gmtPrint("")
    gmtPrint(" (1) Synchronize Google Music and your local files")
    gmtPrint(" (2) Detect and delete duplicated tracks in Google Music")
    gmtPrint(" (3) Generate a playlist with tracks you haven't listened yet")
    gmtPrint(" (4) Insert album arts")
    gmtPrint(" (5) Update list of uploaded files")
    gmtPrint(" (6) Change the music folder (currently " + modules.config.root_path + ")")
    gmtPrint(" (7) Change trash directory")
    gmtPrint(" (8) Change path to credentials")
    gmtPrint(" (9) Change path to list of uploaded files")
    gmtPrint("")
    choice = gmtAskUser("Your choice: ", ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    
    if choice == "1":
        
    elif choice == "2":
        
    elif choice == "3":
        
    elif choice == "4":
        
    elif choice == "5":
        
    elif choice == "6":
        
    elif choice == "7":
        
    elif choice == "8":
        
    elif choice == "9":
        

gmtPrint("Logging out... ", 0)
gmtLogout(obj)
gmtPrint("Done")
