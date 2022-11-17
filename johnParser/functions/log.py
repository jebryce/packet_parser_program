# I wanted a way to print/save more meta info, like the progress of get requests
#
# this prints that information to the console and saves it with a time stamp to 
# the (default) file in the path specified in johnParser/functions/path.py
from datetime import datetime
from johnParser.functions import path

def log(string, filename = 'log.txt', path_to = path.PATH):

    # example time string: '11/15/22 20:22:35 | '
    time = datetime.now().strftime('%m/%d/%y %H:%M:%S | ')

    # 'with' statement closes the file after we are finished with it
    with open(path_to + filename, 'a') as log_file:
        # example of what it writes:
        # 11/15/22 20:22:35 | Created: Documents/johnParser/mac_lookup.txt
        log_file.write(time + string + '\n')

    print(time + string)
