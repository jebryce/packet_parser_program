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
    arg_desc_list = list()
    for arg in args:
        if arg.hex(':').upper() == 'FF:FF:FF:FF:FF:FF':
            arg_desc = 'Broadcast'
        elif arg.hex(':') == '00:00:00:00:00:00':
            arg_desc = 'Target not yet known.'
        else:
            from library import mac_lookup
            assigned_lengths = [6, 7, 9]
            for length in assigned_lengths:
                arg_desc = mac_lookup.mac_lookup.get(
                    arg.hex().upper()[0:length]
                )
                if arg_desc != None:
                    break
        arg_desc_list.append(arg_desc)

    del mac_lookup.mac_lookup
    
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

