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
from library import EtherType_dict

def mac_address_desc(*args):
    # takes in a number of 6 octet mac addresses
    # returns the same number strings with the organization that owns each 
    # respecitive mac address
    #
    # decided to make this a global function as multiple description classes 
    # need descriptions for mac addresses



    file_location = 'library/mac_lookup'
    with open(file_location, 'r', encoding='utf-8') as mac_lookup:

        # arg_desc_list will be returned, will be a list of strings
        arg_desc_list = list()

        # this will be mac addresses that aren't broadcast, and will then be 
        # looked up from table
        no_desc_args = list()


        # first check if mac address is broadcast
        for arg in args:
            if arg.hex(':').upper() == 'FF:FF:FF:FF:FF:FF':
                arg_desc = 'Broadcast'
                arg_desc_list.append(arg_desc)
            elif arg.hex(':') == '00:00:00:00:00:00':
                arg_desc = 'Target not yet known.'
                arg_desc_list.append(arg_desc)
            else:
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
                    arg_desc = row[1].replace('\n', '')
                    arg_desc_list.append(arg_desc)
                    break
    
    # in case mac address isn't found in file
    # note, if you buy a mac block from IEEE (say a six octet block for $3,180),
    # there is an optional yearly fee to have IEEE not publish that you own the 
    # block (for a six octet block it costs $3,675)
    while len(arg_desc_list) != len(args):
        arg_desc_list.append('No Vendor ID found.')

    return arg_desc_list




def EtherTypeDesc(two_octet_field):
    # created as a seperate function as arp shares same descriptions for 
    # protocol type
    #
    # looks up ethertype value in dictionary to find description
    # ex: 'Address Resolution Protocol (ARP)' (type: string)
    ethertype = EtherType_dict.ethertypes.get(
        two_octet_field.hex()
    )                                            
    # if the key in dictionary.get(key) does not exist, it returns None

    # this will probably never get called, but essentially does the same as 
    # previous method, but for rarer ranged ethertypes.
    if ethertype == None:
        for key in EtherType_dict.ranged_ethertypes:

            # if the upper value of the range is greater than the ethertype
            # this works as the dictionary is in incremental order
            if bytes.fromhex(key[5:]) >= two_octet_field:

                # '\' character indicates expression is on next line
                # if the key does not exist it returns the string shown
                ethertype = \
                    EtherType_dict.ranged_ethertypes.get(
                        key, "EtherType was not found"
                    )
                break
    return ethertype
        

class PacketDesc():
    def __init__(self, Packet):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py

        # all self.variables should be strings

        self.packet = 'Raw packet data.'


        self.destination_mac_address, self.source_mac_address = \
            mac_address_desc(
                Packet.destination_mac_address, Packet.source_mac_address
            )

        self.tagged = 'Customer VLAN Tagged Type'
        
        if Packet.tagged == True:
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

