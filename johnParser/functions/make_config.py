# creates a template of a file in the path specified
from johnParser.functions import log

def make_config(path):
    # creates a template of a file in the path specified
    write_path = path + 'config.txt'

    # see johnParser/functions/log.py
    log.log('Creating: ' + write_path)
    
    # opens the file, writes the template.
    # the 'with' statment opens the files then closes it once we are done
    with open(write_path, 'w', encoding='utf-8') as config:
        config.write('# Created using johnParser/functions/make_config.py\n')
        config.write('VLANs\n')
        config.write("\t1 Replace this description at '" + write_path + "'\n")
        config.write("\t02 Replace this description at '" + write_path + "'\n")
        config.write(
            "\t0003 Replace this description at '" + write_path + "'\n"
        )
        config.write(
            '\tXXXX Replace this default description at ' + write_path + '\n'
        )
    
    # see johnParser/functions/log.py
    log.log('Created: ' + write_path)