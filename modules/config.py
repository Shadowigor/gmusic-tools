#!/usr/bin/env python2

import sys
import os.path
from gmusicapi import Musicmanager

def gmtConfigRead(path)
    try:
        with open(path, "r") as file:
            for line in file:
                
                if(line[:17] = "StandardUsername="):
                    conf_std_usr = line[17:]
                    
                elif(line[:15] = "RootDirectiory="):
                    conf_root_dir = line
                    if not os.path.exists(conf_root_dir):
                        sys.stderr.write("Error: Song directory not found\n")
                        return -2
                       
                elif(line[:10] = "TrashPath="):
                    conf_trash_path = line[10:]
                    if not os.path.exists(conf_trash_path):
                        while 1:
                            sys.stdout.write("Couldn't find trash directory. Generate empty one now (y/n)? ")
                            sys.stdout.flush()
                            x = sys.stdin.readline()
                            if(x == "y\n"):
                                try:
                                    os.makedirs(conf_trash_path)
                                except IOError:
                                    sys.stderr.write("Error: Couldn't generate trash directory\n")
                                    return -3
                                break
                            elif(x == "n\n"):
                                print "Error: Trash directory needed"
                                return -4
                            
                elif(line[:16] = "CredentialsPath="):
                    conf_cred_path = line[16:]
                    if not os.path.isfile(conf_cred_path):
                        while 1:
                            sys.stdout.write("Couldn't find credentials. Generate them now (y/n)? ")
                            sys.stdout.flush()
                            x = sys.stdin.readline()
                            if(x == "y\n"):
                                Musicmanager.perform_oauth(cred_path)
                                break
                            elif(x == "n\n"):
                                print "Error: Credentials needed"
                                return -5
                
                elif(line[:17] = "UploadedListPath="):
                    conf_list_path = line[17:]
                    if not os.path.isfile(conf_list_path):
                        while 1:
                            sys.stdout.write("Couldn't find list of uploaded files. Generate empty one now (y/n)? ")
                            sys.stdout.flush()
                            x = sys.stdin.readline()
                            if(x == "y\n"):
                                try:
                                    file = open(conf_list_path, "w")
                                    file.close()
                                except IOError:
                                    sys.stderr.write("Error: Couldn't generate list of uploaded files\n")
                                    return -6
                                break
                            elif(x == "n\n"):
                                sys.stderr.write("Error: List of uploaded files needed\n")
                                return -7
    except IOError:
        sys.stderr.write("Error: Couldn't open config file\n")
        return -1

def gmtConfigWrite(path):
    try:
        with open(path, "w") as file:
            file.write("StandardUsername=" + conf_std_usr + "\n")
            file.write("RootDirectory=" + conf_root_dir + "\n")
            file.write("TrashPath=" + conf_trash_path + "\n")
            file.write("CredentialsPath=" + conf_cred_path + "\n")
            file.write("UploadedListPath=" + conf_list_path + "\n")
    except IOError:
        sys.stderr.write("Error: Couldn't open config file\n")
        return -1
