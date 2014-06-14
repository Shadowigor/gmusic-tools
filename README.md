###Because the whole file structure is reorganized at the moment, the program won't work properly. Please wait until the restructuring process is done or get a previous version.

##gmusic-tools: Scripts for Google Play Music
gmusic-tools contains scripts for a more powerful management of [Google
Music](https://music.google.com/). They are all completely written in Python and are based upon the [unofficial
gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API).

__gmusic-tools is not supported by Google in any way.__

The main features are the following ones:

* Synchronize your music
    * Uploads new music that you add to your local library
    * Deletes local files that were deleted in Google Music
    * Deletes tracks in Google music that were deleted locally
    * Doesn't care about 'Album Artist' -> Less duplicated uploads
    * Local files will be moved to a trash directory instead of being permanently deleted
* Detect and delete duplicates
    * Removes duplicates from Google Music
    * Doesn't care about 'Album Artist' (Unlike Google's Music Manager)
    * Preserves how many times you have listened to a track (still in development, dont' rely on it!)
    * Deletes the older file
* Create a playlist with tracks you haven't listened to yet
* Insert album arts
    *  Searches for local image files in the music folder
    * If nothing is found, search the internet for it

##Getting started
### Install dependencies
To use this scripts you will need python and the gmusicapi. 

To install python type in the following command (Ubuntu only):

sudo apt-get install python

The scripts only work with python2 (yet) and not with python3. To install the gmusicapi type in the following command:

pip install gmusicapi

Please refer to the [gmusicapi
documentation](http://unofficial-google-music-api.readthedocs.org/en/latest/usage.html#installation) for additional
informations.

### Usage
To start the programm, change to to gmusic-tool directory and enter the following command:

python2 gmt.py

The programm itself should be quite self-explanatory.

##To-Do's
The following features will (hopefully) be in future releases:

* Case insensitive duplicate detection
* Add a GUI
_____________________________________________________________________

This program is licenced under the GPLv3. See LICENCE.
