# This is to automake making description lookup files, see individual functions 
# for more info
# 
# found ethertypes, mac addresses from:
# https://standards.ieee.org/products-programs/regauth/
# 
# 

import requests
import csv
from PPP.functions import log, path


def request_to_file(write_path, data_remover_function, *urls):
    # takes in any amount of urls (to csv files (excel, spreadsheet data 
    # format), creates a file at write_path, then passes each row of the csv
    # file through data_remover_function
    #
    # example write_path: (type: string)
    # '/Users/john/Documents/PPP/mac_lookup.txt'
    #
    # example data_remover_function: (type: (custom) function)
    # data_remover_mac          (see function declaration below)
    #
    # example urls: (type: string) (as many strings as you want)
    # 'http://standards-oui.ieee.org/oui/oui.csv'


    # 'with' statement closes session after we are finished with it
    with requests.Session() as request_session:
        with open(write_path, 'w', encoding='utf-8') as lookup_file:

            # write a breadcrumb? back to here if anyone is curious
            lookup_file.write(
                '# Created using PPP/functions/make_lookups.py\n'
            )

            # iterate through the passed urls
            for url in urls:


                # tell the human we are making progress, as making some of the 
                # lookup files takes a while
                #
                # see PPP/functions/log.py (writes to file in the same 
                # directory as these lookup files)
                log.log("\tRequesting csv file from: '{}'".format(url))

                # this is janky, I wanted to process the spreadsheet by loading 
                # each row into memory individually, instead of loading the 
                # entire spreadsheet at once (to save memory)
                #
                # I ran into a problem where if the cell of memory in the 
                # spreadsheet had a newline character, then the .iter_lines() 
                # would count that as a newline itself and not as part of the 
                # string occupying that cell. 
                #
                # For example the spreadsheet row might be: 
                # 'Assignment,"Description \n with a newline"\n'
                # and the iter_lines() would break that into two lines instead 
                # of one. 
                # 
                # This buffer is to hold the current partial row until the 
                # program has found the entire row. 
                # 
                # Extending this previous example, buffer would store:
                # 'Assignment,"Description', 
                # then the next iteration would add the rest of the row to this 
                # buffer with the result of 
                # 'Assignment,"Description with a newline"'
                buffer = ''
                
                # makes the physical request to the url for it's data
                #
                # since I passed stream = True, the data will be processed as 
                # the computer receives it, and the .iter_lines() call breaks 
                # into lines to process
                for raw_row in request_session.get(
                    url, stream = True
                ).iter_lines():
                
                    # see description above for what buffer does,
                    #
                    # raw_row is received as a bytes object, this also decodes 
                    # it into text (utf-8)
                    #
                    # type is now a string
                    raw_row = buffer + raw_row.decode('utf-8')
                    
                    # this is how I checked if I received a full row or a 
                    # partial one 
                    #
                    # basically if there was a newline in a cell, then the csv 
                    # format would save the contents of that cell surrounded 
                    # with double quotes, so if the .iter_lines() provides a 
                    # string with an odd number of " characters, then it must 
                    # be a partial row 
                    # 
                    # (aka the number of " characters mod 2 = 1)
                    if raw_row.count('"') % 2 == 1:
                        # store the partial row in the buffer (type: string)
                        buffer = raw_row + ' '

                    # for some reason iter_lines() would send a blankline,
                    # if so then we ignore it
                    elif raw_row != '':
                        # csv.reader() cannot take a string as input, so we 
                        # convert it to a list, and it returns a csv.reader() 
                        # object, so .__next__() returns a list containg the 
                        # spreadsheet row's contents
                        #
                        # the .__next__() is enough as the csv.reader object 
                        # only was passed one row
                        #
                        # variable 'row' is type list
                        row = csv.reader([raw_row]).__next__()
                        
                        # since row is a list, the function does not have to 
                        # return anything, but the way I have it set up, the 
                        # function needs to return something (True) and if we 
                        # want to skip a row, we can return False and it
                        # won't write anything to the file
                        #
                        # lists are 'changeable' so the variable that is passed 
                        # to the data_remover_function, is the same variable 
                        # that is written to the file
                        if data_remover_function(row):
                            # joins each item in the list row, with a 
                            # seperation of a space
                            lookup_file.write(' '.join(row) + '\n')

                        # reset buffer for next potential split line
                        buffer = ''
    # In case you are wondering if processing the data as we get it takes 
    # longer or how much memory it really saves, I tested it, and from 
    # processing the 31925 line spreadsheet from url 'http://standards-oui.ieee.
    # org/oui/oui.csv' 5 times with the method as shown, and the previous 
    # method (not shown, but it just loaded the entire received spreadsheet 
    # into memory then processed it) I found the following statistics:
    #
    # on average the old method used 30.05 MB of memory and took 2.994 secs
    # 
    # on average the new method used 4.044 MB of memory and took 3.285 secs
    #
    # new/old (what fraction of the old does the new take)
    # new/old memory = 0.1346, new/old time = 1.09719
    #
    # for percentage multiples: 
    # memory = old/new * 100%, old method takes 743% more memory
    # memory = new/old * 100%, new method takes 13.46% the memory
    # time = old/new * 100%,       old method took 91.1% the time
    # time = (new/old - 1) * 100%, new method takes 9.72% longer

    
def make_mac_lookup():
    # sets up the call to the request_to_file function for the mac address 
    # lookup file

    # Where the mac address lookup table will be located
    write_path = PATH + 'mac_lookup.txt'

    # see PPP/functions/log.py
    log.log('Creating: ' + write_path)

    # csv files that we will download to create a file of vendor IDs
    urls = [
        'http://standards-oui.ieee.org/oui/oui.csv',
        'http://standards-oui.ieee.org/oui28/mam.csv',
        'http://standards-oui.ieee.org/oui36/oui36.csv',
        'http://standards-oui.ieee.org/iab/iab.csv',
        'http://standards-oui.ieee.org/cid/cid.csv'
    ]

    # see the function request_to_file for more info
    request_to_file(write_path,data_remover_mac,*urls)

    # see PPP/functions/log.py
    log.log('Created: ' + write_path)

def data_remover_mac(list_row):
    # see functions make_mac_lookup and request_to_file

    # list_row will start as something like:
    # ['Registry', 'Assignment', 'Organization Name', 'Organization Address']
    # then removes the third (last) and first entries to end up with:
    # ['Assignment', 'Organization Name']
    list_row.pop(3)
    list_row.pop(0)

    # returns true to print to file
    return True

def make_ethertype_lookup():
    # (re)generates a file that contains ethertypes and their descriptions

    # Where the mac address lookup table will be located
    write_path = PATH + 'ethertype_lookup.txt'

    # see PPP/functions/log.py
    log.log('Creating: ' + write_path)

    # csv file we will download to get the ethertypes with descriptions
    url = 'http://standards-oui.ieee.org/ethertype/eth.csv'

    # see the function request_to_file for more info
    request_to_file(write_path,data_remover_ethertype,url)
    
    # see PPP/functions/log.py
    log.log('Created: ' + write_path)

def data_remover_ethertype(list_row):
    # see functions make_ethertype_lookup and request_to_file

    # if this isn't added, there would be ~3287 lines that have 'Protocol 
    # unavailable.' as a description (which obviously isn't very helpful), this 
    # decreases the number of lines by 90%
    if list_row[4] == 'Protocol unavailable.':
        # returns False to not print to file
        return False

    # for some ethertypes, they are presented as ="88E4" in the csv file 
    # (this is because without the quotes: 88E4 = 88 * 10^4)
    elif len(list_row[1]) != 4:
        # list_row[1] goes from ="88E4" to '88E4'
        list_row[1] = list_row[1][2:6]
    
    # list_row will start as something like:
    # ['Registry', 'Assignment', 'Organization Name', 'Organization Address', 
    # 'Protocol']
    # then removes the fourth, third, and first entries to end up with:
    # ['Assignment', 'Protocol']
    list_row.pop(3)
    list_row.pop(2)
    list_row.pop(0)

    # returns true to print to file
    return True

def make_arp_opcode_lookup():
    # (re)generates a file that contains ethertypes and their descriptions

    # Where the mac address lookup table will be located
    write_path = PATH + 'arp_opcode_lookup.txt'

    # see PPP/functions/log.py
    log.log('Creating: ' + write_path)

    # csv file we will download to get the ethertypes with descriptions
    url = 'https://www.iana.org/assignments/arp-parameters/arp-parameters-1.csv'

    # see the function request_to_file for more info
    request_to_file(write_path,data_remover_arp_opcode,url)
    
    # see PPP/functions/log.py
    log.log('Created: ' + write_path)


def data_remover_arp_opcode(list_row):
    if '-' in list_row[0]:
        # if csv has a range of values, don't bother writing it to file
        # ex: ['26-65534', 'Unassigned']
        # retursn false to not print to file
        return False
    # remove the third entry
    list_row.pop(2)
    # will go from:
    # ['Number', 'Operation Code (op)', 'References']
    # to:
    # ['Number', 'Operation Code (op)']
    
    # returns true to print to file
    return True

def make_arp_hardware_lookup():
    # (re)generates a file that contains ethertypes and their descriptions

    # Where the mac address lookup table will be located
    write_path = PATH + 'arp_hardware_lookup.txt'

    # see PPP/functions/log.py
    log.log('Creating: ' + write_path)

    # csv file we will download to get the ethertypes with descriptions
    url = 'https://www.iana.org/assignments/arp-parameters/arp-parameters-2.csv'

    # see the function request_to_file for more info
    request_to_file(write_path,data_remover_arp_hardware,url)
    
    # see PPP/functions/log.py
    log.log('Created: ' + write_path)


def data_remover_arp_hardware(list_row):
    if '-' in list_row[0]:
        # if csv has a range of values, don't bother writing it to file
        # ex: ['258-65534', 'Unassigned']
        # retursn false to not print to file
        return False
    # remove the third entry
    list_row.pop(2)
    # will go from:
    # ['Number', 'Hardware Type (hrd)', 'Reference']
    # to
    # ['Number', 'Hardware Type (hrd)']

    # returns true to print to file
    return True

def make_lookups(path):
    # this is for testing, will be removed when implemented fully.
    global PATH
    PATH = path
    make_mac_lookup()
    make_ethertype_lookup()
    make_arp_opcode_lookup()
    make_arp_hardware_lookup()
