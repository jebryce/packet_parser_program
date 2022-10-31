# Wireshark downloads csv files from IEEE to show MAC address owners, idea is 
# to do something similar.
#
# https://standards.ieee.org/products-programs/regauth/
# 
# 

import requests
import csv


def get_list_from_url(url):
    # takes in a url to a csv file, returns a list containing the data of the 
    # csv file (minus the first row)

    # 'with' statement closes session after we are finished with it
    with requests.Session() as request_session:
        # This is a lengthy process, and this file requests multiple csv files, 
        # this is just used to tell the human it hasn't frozen
        print("Requesting csv file from: '{}'".format(url))

        # makes the physical request to the url for it's data
        response = request_session.get(url)

        # converts response object to raw (text) data
        csv_response = response.text

        #converts raw (text) data to a python list
        editted_csv_response = list(csv.reader(csv_response.splitlines()))

        # removes the title row:
        editted_csv_response.pop(0)
    return editted_csv_response
    
def make_mac_lookup():
    # Where the mac address lookup table will be located
    write_path = 'library/mac_lookup'

    # TODO: create logger :/
    print('Creating', write_path)

    # (re)generates a file that contains a dictionary of MAC Vendor IDs
    urls = {
        'MAC Address Block Large (MA-L)' : \
            'http://standards-oui.ieee.org/oui/oui.csv',

        'MAC Address Block Medium (MA-M)' : \
            'http://standards-oui.ieee.org/oui28/mam.csv',

        'MAC Address Block Small (MA-S)' : \
            'http://standards-oui.ieee.org/oui36/oui36.csv',
        
        'Individual Address Block (IAB)' : \
            'http://standards-oui.ieee.org/iab/iab.csv',
        
        'Company ID (CID)' : 'http://standards-oui.ieee.org/cid/cid.csv',
    }

    # this will be populated by nested lists that contain a 6-9 octet string 
    # (the first 6-9 octets of a MAC address), and the respective Organization 
    # that owns it 
    # ex: [ ['00D0EF', 'IGT'], ['405582', 'Nokia'] ]
    all_vendor_ids = list()

    for url_key in urls:
        # vendor_ids would be a list of lists, with the following date in each 
        # nested list: 
        # Registry, Assignment, Organization Name, Organization Address
        # (Assignment is a 6-9 octet string - the first 6-9 octets 
        # of a MAC address)
        # ex: MA-L, 405582, Nokia, 600 March Road Kanata Ontario CA K2K 2E6 
        vendor_ids = get_list_from_url(urls[url_key])

        for row in vendor_ids:
            # removes the first and last items of each row - effectively 
            # removing the first (Registry) and last (Organization Address) 
            # columns of the original csv file
            row.pop()
            row.pop(0)

            # after edtting, vendor_ids is still a list of lists, but each 
            # nested list now contains a 6-9 octet string (the first 6-9 octets 
            # of a MAC address), and the respective Organization that owns it 
            # ex: [ ['00D0EF', 'IGT'], ['405582', 'Nokia'] ]

            # consolidates all the csv data from the multiple urls
            all_vendor_ids.append(row)

    with open(write_path, 'w', encoding='utf-8') as mac_lookup_file:
        mac_lookup_file.write('# Created using /library/makeDescriptions.py\n')
        for row in all_vendor_ids:
            mac_lookup_file.write(row[0]+' '+row[1]+'\n')

    # TODO: create logger :/
    print(write_path, 'created')




def main():
    make_mac_lookup()
    






main()