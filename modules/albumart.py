import urllib2
import simplejson
import modules.error as error
from modules.misc import *

def gmtGetAlbumArtURL(track, path):
    error.e = 0

    try:
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + 
               urllib2.quote(track["artist"] + " " + track["album"] + " album cover"))
        gmtPrintVVV("gmtDownloadAlbumArt: Request: " + url)
    except:
        error.e = error.INVALID_ARGUMENT
        gmtFatal("Invalid Argument")
    
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
#        response = urllib2.urlopen(results["responseData"]["results"][0]["url"])
    except:
        error.e = error.WEB_ERROR
        gmtPrintV("gmtDownloadAlbumArt: Error while downloading album art")
        return
    
    track["albumArtUrl"] = results["responseData"]["results"][0]["url"]
    return track
#     try:
#         with open(path, "w") as file:
#             file.write(response.read())
#     except:
#         error.e = error.FILE_ERROR
#         gmtPrintV("gmtDownloadAlbumArt: Error while saving album art")
