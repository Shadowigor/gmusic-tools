#!/usr/bin/env python2

from gmusicapi import Mobileclient
from gmusicapi import Webclient
from gmusicapi import Musicmanager
from modules.misc import *
import modules.error as error
import modules.config as config

class gmObject:
    
    def __init__(self):
        self.mc = Mobileclient()
        self.wc = Webclient()
        self.mm = Musicmanager()
    
    def login(self, username, password):
        error.e = 0
        
        if not self.mc.login(username, password):
            gmtPrintV("gmObject.login: Wrong username or password (or no internet connection)")
            error.e = error.LOGIN_FAILED
            return
        
        if not self.wc.login(username, password):
            gmtPrintV("gmObject.login: Wrong username or password (or no internet connection)")
            error.e = error.LOGIN_FAILED
            return
        
        if not self.mm.login(config.cred_path):
            gmtPrintV("gmObject.login: Wrong credentials (or no internet connection)")
            error.e = error.LOGIN_FAILED
            return
        
    def logout(self):
        error.e = 0
        
        try:
            self.mc.logout()
            self.wc.logout()
            self.mm.logout()
        except:
            gmtPrintV("gmObject.logout: Logout failed")
            error.e = error.LOGOUT_FAILED
