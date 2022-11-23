# see /functions/sdnParser.py for more detail
#
# This exists really only for humans. The /functions/sdnParser.py file from 
# which this is called, parses all the information a computer needs. But we 
# (hopefully) aren't computers and this function creates English strings that 
# describe what the parsed data represents. 
#
# This file contains all description subclasses the main 'Packet' class 
# creates.
#
# A way to call the description variable, for example:
# my_Packet = Packet(bytes), where bytes is a packet of type bytes
# my_Packet.ethertype                  | returns a bytes object
#                                      | ex: 0806 (type: bytes)
# my_Packet.desc.ethertype             | returns a string that describes
#                                      | ex: 'Address Resolution Protocol (ARP)'
# my_Packet.arp.opcode                 | returns a bytes object
#                                      | ex: 01 (type: bytes)
# my_Packet.arp.desc.opcode            | returns a string that describes
#                                      | ex: 'Request' (type: string)
# generally:                           |
# my_Packet.variable                   | calls the data of variable
# my_Packet.desc.variable              | calls the description of variable
#
import os
from johnParser.functions import path
PATH = path.PATH

class Packet_desc():
    def __init__(self, Packet):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py

        # all self.variables should be strings

        # initialize all Ethernet frame variables to be None.
        # this is done so that if a ethertype description needs to open a file 
        # for say, ARP sender/target mac addresses, then the arp description 
        # class can open the file once and receive all four mac addresses, (ARP 
        # sender, ARP target, ethernet source, and ethernet destination) 
        # instead of opening the file twice and receive each pair indiviudally
        self.packet = None
        self.source_mac_address = None
        self.destination_mac_address = None
        if Packet.tagged != False:
            self.tagged = None
            self.vlan_id = None
        self.ethertype = None
    
    def finish_descriptions(self, Packet):
        # from reasoning above, if the ethernet frame descriptions haven't been 
        # set, fill them in
        if self.packet == None:
            self.packet = 'Raw packet data.'

        # backslahes mean the expression is continued on the next line
        # this is hard to read, so:
        # if both ethernet mac address descriptions are Nonetype
        if self.destination_mac_address == None and \
            self.source_mac_address == None:

            # then call self.mac_address_lookup with the mac addresses
            mac_addresses = self.mac_address_lookup(
                    Packet.destination_mac_address, Packet.source_mac_address
                )
            # then assign the descriptions to the self.var
            self.destination_mac_address = \
                mac_addresses[Packet.destination_mac_address]
            self.source_mac_address = \
                mac_addresses[Packet.source_mac_address]
        
        if Packet.tagged != False:
            if self.tagged == None:
                self.tagged = 'Customer VLAN Tagged Type' 
            if self.vlan_id == None:
                self.vlan_id = \
                    self.vlan_id_lookup(Packet.vlan_id)[Packet.vlan_id]

        if self.ethertype == None:
            self.ethertype = \
                self.ethertype_lookup(Packet.ethertype)[Packet.ethertype]


    def vlan_id_lookup(self, *vlan_ids):
        # takes in a number of 2 octet vlan_ids
        # returns a dictionary of the same number of strings with a 
        # configurable description taken from ~/Documents/johnParser/config
        # where '~' is user
        #
        # NOTE: this needs to be updated, the reasoning is that it tries to 
        # iterate over the entire file for each vlan id - and not the other way 
        # around
        # this doesn't work because if the 'for row in config' gets to row 50 
        # then we break, for next vlan_id it needs to lookup, it starts from 
        # row 51 - which is annoying so go look at the mac_address_lookup 
        # function to see how i fixed this


        # 'with' closes the file after we are finished with it
        config_file = PATH + 'config.txt'
        with open(config_file, 'r',  encoding='utf-8') as config:

            # shortened vlan_id to vid
            # vid_descs will be returned, will be key = X.desc.X variable 
            # provided, and value = description
            vid_descs = dict()

            # this was my first attempt at writing a config file
            found_VLANs = False
            for vlan_id in vlan_ids:
                for row in config:
                    # so first we search for the line 'VLANS\n'
                    if found_VLANs == False and row == 'VLANs\n':
                        # once we have found it, latch this boolean
                        found_VLANs = True
                    # now start searching every line for our vlan description
                    elif found_VLANs == True:
                        # if the line starts with a tab, then continue
                        if row[0] == '\t':
                            # turn row: '\t0003 This is our vlan description!\n'
                            # into ['0003', 'This is our vlan descrption!\n']
                            row = row.replace('\t','').split(' ', 1)
                            # zfill fills in zeros from the left
                            # ex: 3 -> 0003
                            if row[0].zfill(4) == vlan_id.hex().upper():
                                # if we found what we were looking for, break 
                                vid_descs[vlan_id] = row[1].replace('\n', '')
                                break
                            elif row[0] == 'XXXX':
                                # 'XXXX' I implemented as a general description
                                vid_descs[vlan_id] = row[1].replace('\n', '')
                        # once we reach the end of the VLANs data, break
                        else:
                            break
        return vid_descs

    def mac_address_lookup(self, *addresses):
        # takes in a number of 6 octet mac addresses
        # returns a dictionary of the same number of strings with the 
        # organization that owns each respecitive mac address

        # address_descs will be returned, will be key = X.desc.X variable 
        # provided, and value = description
        address_descs = dict()
        # note that dictionaries do not allow duplicate values, so if 4 
        # addresses are passed, then a dictionary of length 3 is returned
        
        # sets also do not allow duplicate values. This is nice so that we 
        # don't have to lookup the same value twice
        addresses = set(addresses)

        # I compare the length of the dictionary at the end, and if they are 
        # seperate lengths, then I add in default descriptions until the 
        # lengths match
        num_addresses = len(addresses)

        # first check if any address is to broadcast 
        broadcast = bytes.fromhex('FFFFFFFFFFFF')
        if broadcast in addresses:
            # if it is, add it to the descriptions and remove it from the set
            address_descs[broadcast] = 'Broadcast'
            addresses.remove(broadcast)

        # similarly, check if any address is all zero
        no_target = bytes.fromhex('000000000000')
        if no_target in addresses:
            address_descs[no_target] = 'Target not yet known.'
            addresses.remove(no_target)

        # if we still have addresses (which we probably always will)
        if len(addresses) > 0:

            # 'with' closes the file after we are finished with it
            mac_lookup_file = PATH + 'mac_lookup.txt'
            with open(mac_lookup_file, 'r', encoding='utf-8') as mac_lookup:
                for row in mac_lookup:
                    # splits each row into a list of two values, first 
                    # value is the address block assigned, and the second 
                    # vlaue is the organization that owns the address block
                    # ex: ['0001C7', 'Cisco Systems, Inc\n'] (type:list)
                    row = row.split(' ', 1)

                    # length of address block assigned to organization
                    # ex: 6 (type: int) (this can only be 6, 7, or 9)
                    assigned_length = len(row[0])

                    # for each remaining address, see if the current row matches
                    for address in addresses:
                        # if the first assigned_length hex numbers match
                        if address.hex().upper()[:assigned_length] == row[0]:
                            # then add the description to the dictionary
                            address_descs[address] = row[1].replace('\n', '')
                        
                    # this break is here and not in the if statement above 
                    # in case there are two (or more) mac addresses from the 
                    # same organization 
                    if len(address_descs) == num_addresses:
                        break

                # if we have gone through the entire file and there are still 
                # some addresses without descriptions, add in a default
                if len(address_descs) != num_addresses:
                    # of the remaining addresses
                    for address in addresses:
                        # if they don't have a description
                        if address not in address_descs:
                            # add this default one
                            address_descs[address] = 'No vendor ID found.'
        
        return address_descs

    def ethertype_lookup(self, *ethertypes):
        # takes in a number of 2 octet ethertypes
        # returns the same number of strings with the 
        #
        # NOTE: this needs to be updated, see vlan_id_lookup for reasoning

        # 'with' closes the file after we are finished with it
        ethertype_lookup_file = PATH + 'ethertype_lookup.txt'
        with open(ethertype_lookup_file, 'r', encoding='utf-8') as \
            ethertype_lookup:

            # arg_desc_dict will be returned, will be key = X.desc.X variable 
            # provided, and value = description
            ethertype_descs = dict()  


            for ethertype in ethertypes:
                ethertype_descs[ethertype] = 'Protocol unavailable.'
                for row in ethertype_lookup:
                    # splits each row into a list of two values, first value is
                    # the ethertype, and the second vlaue is the description
                    # ex: (type: list)
                    # ['0806', 'Address Resolution Protocol - A. R. P.\n']
                    row = row.split(' ', 1)
                    if ethertype.hex().upper() == row[0]:
                        ethertype_descs[ethertype] = row[1].replace('\n','')
                        break

        return ethertype_descs
                    

        
class Arp_desc():
    def __init__(self,Arp,Packet):
        # TODO import IANA spreadsheet for hardware type
        self.hardware_type = 'placeholder for hardware_type lookup'

        # this shares the same EtherType numbers/descriptions
        # so lookup all ethertypes
        ethertypes = Packet.desc.ethertype_lookup(
            Arp.protocol_type,
            Packet.ethertype
        )
        # then assign them to the correct variables
        self.protocol_type = ethertypes[Arp.protocol_type]
        Packet.desc.protocol_type = ethertypes[Packet.ethertype]

        self.hardware_size = 'Length of the hardware (MAC) address.'

        self.protocol_size = 'Length of the network protocol (IPv4) address.'

        # TODO import IANA spreadsheet for opcode
        self.opcode = 'placeholder for opcode lookup'

        # lookup mac addresses
        mac_addresses = Packet.desc.mac_address_lookup(
            Packet.source_mac_address,
            Packet.destination_mac_address,
            Arp.sender_mac_address,
            Arp.target_mac_address
        )
        # then assign then to the correct variables
        Packet.desc.source_mac_address = \
            mac_addresses[Packet.source_mac_address]
        Packet.desc.destination_mac_address = \
            mac_addresses[Packet.destination_mac_address]
        self.sender_mac_address = mac_addresses[Arp.sender_mac_address]
        self.target_mac_address = mac_addresses[Arp.target_mac_address]



        # TODO implement ip address lookup
        self.sender_ip_address = 'placeholder for IP lookup'
        self.target_ip_address = 'placeholder for IP lookup'

