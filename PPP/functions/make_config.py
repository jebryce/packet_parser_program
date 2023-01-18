# I wanted a way to keep this library generic - i.e. not have any unique 
# details to my implementation in the github repo - so for things like VLAN 
# names, I still wanted to be able to print our custom names, but not have 
# anyone who decides to use this repo to be stuck with ours
#
# This creates a text file so that a user can replace the generic vlan names

from PPP.functions import log

def make_config(path):

    write_path = path + 'config.txt'

    # see PPP/functions/log.py
    log.log('Creating: ' + write_path)
    
    # write a template so that users know what to edit
    # the 'with' statment opens the files then closes it once we are done
    with open(write_path, 'w', encoding='utf-8') as config:
        config.write('# Created using PPP/functions/make_config.py\n')
        config.write('VLANs\n')
        config.write("\t1 Replace this description at '" + write_path + "'\n")
        config.write("\t02 Replace this description at '" + write_path + "'\n")
        config.write(
            "\t0003 Replace this description at '" + write_path + "'\n"
        )
        config.write(
            '\tXXXX Replace this default description at ' + write_path + '\n'
        )
    
    # see PPP/functions/log.py
    log.log('Created: ' + write_path)