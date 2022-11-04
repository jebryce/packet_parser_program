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
PATH = os.getcwd()

def mac_address_desc(*args):
    # takes in a number of 6 octet mac addresses
    # returns the same number strings with the organization that owns each 
    # respecitive mac address
    #
    # decided to make this a global function as multiple description classes 
    # need descriptions for mac addresses



    mac_lookup_file = PATH+'/library/mac_lookup'
    with open(mac_lookup_file, 'r', encoding='utf-8') as mac_lookup:

        # arg_desc_dict will be returned, will be key = X.desc.X variable 
        # provided, and value = description
        arg_desc_dict = dict()

        # this will be mac addresses that aren't broadcast, and will then be 
        # looked up from table
        no_desc_args = list()


        # first check if mac address is broadcast
        for arg in args:
            if arg.hex(':').upper() == 'FF:FF:FF:FF:FF:FF':
                arg_desc_dict[arg] = 'Broadcast'
            elif arg.hex(':') == '00:00:00:00:00:00':
                arg_desc_dict[arg] = 'Target not yet known.'
            else:
                # in case mac address isn't found in file. Note: if you buy a 
                # mac block from IEEE (say a six octet block for $3,180), there 
                # is an optional yearly fee to have IEEE not publish that you 
                # own the block (for a six octet block it costs $3,675)
                arg_desc_dict[arg] = 'No Vendor ID found.'
                no_desc_args.append(arg)

        # if mac address isn't broadcast, lookup from file
        for arg in no_desc_args:
            for row in mac_lookup:
                # splits each row into a list of two values, first value is the 
                # address block assigned, and the second vlaue is the 
                # organization that owns the address block
                # ex: ['0001C7', 'Cisco Systems, Inc\n'] (type:list)
                row = row.split(' ', 1)

                # length of address block assigned to organization
                # ex: 6 (type: int) (this can only be 6,7, or 9)
                assigned_length = len(row[0])

                if arg.hex().upper()[:assigned_length] == row[0]:
                    arg_desc_dict[arg] = row[1].replace('\n', '')
                    break

    return arg_desc_dict




def EtherTypeDesc(two_octet_field):
    # created as a seperate function as arp shares same descriptions for 
    # protocol type
    ethertype_lookup_file = PATH+'/library/ethertype_lookup'

    
    description = 'Protocol unavailable.'
    with open(ethertype_lookup_file, 'r', encoding='utf-8') as ethertype_lookup:
        for row in ethertype_lookup:
            # splits each row into a list of two values, first value is the 
            # ethertype, and the second vlaue is the description
            # ex: (type: list)
            # ['0806', 'Address Resolution Protocol - A. R. P.\n']
            row = row.split(' ', 1)
            if two_octet_field.hex().upper() == row[0]:
                description = row[1].replace('\n', '')
                break

    return description
            


class PacketDesc():
    def __init__(self, Packet):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py

        # all self.variables should be strings

        self.packet = 'Raw packet data.'


        mac_addresses = mac_address_desc(
                Packet.destination_mac_address, Packet.source_mac_address
            )
        self.destination_mac_address = \
            mac_addresses[Packet.destination_mac_address]
        self.source_mac_address = \
            mac_addresses[Packet.source_mac_address]
        
        if Packet.tagged == True:
            self.tagged = 'Customer VLAN Tagged Type' 
            # TODO: create vlan ID lookup
            self.vlan_id = 'SDN Production VLAN'

        # looks up ethertype value in dictionary to find description
        # ex: 'Address Resolution Protocol (ARP)' (type: string)
        self.ethertype = EtherTypeDesc(Packet.ethertype)
        
class arpDesc():
    def __init__(self,arp):
        # TODO import IANA spreadsheet for hardware type
        self.hardware_type = 'placeholder for hardware_type lookup'

        # this shares the same EtherType numbers/descriptions
        self.protocol_type = EtherTypeDesc(arp.protocol_type)

        self.hardware_size = 'Length of the hardware (MAC) address.'

        self.protocol_size = 'Length of the network protocol (IPv4) address.'

        # TODO import IANA spreadsheet for opcode
        self.opcode = 'placeholder for opcode lookup'

        # TODO use same lookup as base packet class
        self.sender_mac_address = 'placeholder for mac lookup'

        # TODO implement ip address lookup
        self.sender_ip_address = 'placeholder for IP lookup'

        # TODO use same lookup as base packet class
        self.target_mac_address = 'placeholder for mac lookup'

        # TODO implement ip address lookup
        self.target_ip_address = 'placeholder for IP lookup'

