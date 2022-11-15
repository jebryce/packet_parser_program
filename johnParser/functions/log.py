from datetime import datetime
from johnParser.functions import path

def log(string, filename = 'log.txt', path_to = path.PATH):
    time = datetime.now().strftime('%m/%d/%y %H:%M:%S | ')
    with open(path_to + filename, 'a') as log_file:
        log_file.write(time + string + '\n')
    print(string)
