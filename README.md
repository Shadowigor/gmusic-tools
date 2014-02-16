##gmusic-sync: Synchronisation scripts for Google Play Music
gmusic-sync contains scripts for a more powerful synchronisation of your local files with [Google
Music](https://music.google.com/). They are all completely written in Python and are based upon the [unofficial
gmusicapi](https://github.com/simon-weber/Unofficial-Google-Music-API).

__gmusic-sync is not supported by Google in any way.__

The main features are the following ones:

* sync.py
    * Uploads new music that you add to your local library
    * Deletes local files that were deleted in Google Music
    * Deletes tracks in Google music that were deleted locally
    * Doesn't care about 'Album Artist' -> Less duplicated uploads
    * Local files will be moved to a trash directory instead of being permanently deleted
* duplicates.py
    * Removes duplicates from Google Music
    * Doesn't care about 'Album Artist' (Unlike Google's Music Manager)
    * Preserves how many times you have listened to a track (The bigger value is chosen) (still in development)
    * Deletes the older file

##Getting started
### Install dependencies
To use this scripts you will need python and the gmusicapi. 

To install python type in the following command (Ubuntu only):

sudo apt-get install python

To install the gmusicapi type in the following command:

pip install gmusicapi

Please refer to the [gmusicapi
documentation](http://unofficial-google-music-api.readthedocs.org/en/latest/usage.html#installation) for additional
informations.

### Usage
#### sync.py
To use sync.py, you first have to edit it. At the top of the file are 4 file paths which you may have to edit. The
most important one is 'rootdir'. This is the directory on your computer where all your music is stored. It will be
searched recursively. The defaults are fine for all other variables, but you can change them if you like.

To start sync.py, just type in the following command while you're in the gmusic-sync directory:

python sync.py

The program itself should be self-explanatory. Note, that if it says 'Local files deleted', that the files aren't
really deleted. They are moved to the trash directory. This should prevent you from accidently delete something you
wanted to keep.

#### duplicates.py
To use duplicates.py you simply have to execute the following command:

python duplicates.py

This program should also be self-explanatory.

##To-Do's
The following features will (hopefully) be in future releases:

* Save the login informations in a file
* Choose what changes you want to execute
* Case insensitive duplicate detection
* Integrate duplicates.py in sync.py
* Add a menu
_____________________________________________________________________

This program is licenced under the GPLv3. See LICENCE.
