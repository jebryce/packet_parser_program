# for testing
# want to initialize ~/Library/johnParser
# want to initialize logger
# want to initialize description lookups
# want to initialize config file


import os
from johnParser.functions import path, make_lookups, make_config

PATH = path.PATH

def create_library_folder():
    # checks if the johnParser folder exists yet
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
make_library()