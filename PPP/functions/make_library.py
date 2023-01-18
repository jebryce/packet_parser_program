# this is a convenience function that may or may not be replaced
#
# it creates a folder at PATH, then populates that folder with calls to 
# math_lookups.py and make_config.py

import os
from PPP.functions import path, make_lookups, make_config

PATH = path.PATH

def create_library_folder():
    # checks if the PPP folder exists yet
    if os.path.exists(PATH) == False:
        # if it doesn't, try making it
        try:
            os.mkdir(PATH)
            print('Created: ' + PATH)
        except:
            print('Failed creating: ' + PATH)

def make_library():
    # for testing atm
    create_library_folder()
    make_lookups.make_lookups(PATH)
    make_config.make_config(PATH)