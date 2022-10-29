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

class PacketDesc():
    def __init__(self, Packet):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py

        # all self.variables should be strings

        self.packet = 'Raw packet data.'

        # TODO: create MAC address vendor ID lookup
        self.destination_mac_address = "dest mac addr placeholder"
        self.source_mac_address = "source mac addr placeholder"

        self.tagged = 'Customer VLAN Tagged Type'
        
        if Packet.tagged == True:
            # TODO: create vlan ID lookup
            self.vlan_id = 'SDN Production VLAN'

        
        
        # looks up ethertype value in dictionary to find description
        # ex: 'Address Resolution Protocol (ARP)' (type: string)
        self.ethertype = EtherType_dict.ethertypes.get(
            Packet.ethertype.hex()
        )                                            
        # if the key in dictionary.get(key) does not exist, it returns None

        # this will probably never get called, but essentially does the same as 
        # previous method, but for rarer ranged ethertypes.
        if self.ethertype == None:
            for key in EtherType_dict.ranged_ethertypes:

                # if the upper value of the range is greater than the ethertype
                # this works as the dictionary is in incremental order
                if bytes.fromhex(key[5:]) >= Packet.ethertype:

                    # '\' character indicates expression is on next line
                    # if the key does not exist it returns the string shown
                    self.ethertype = \
                        EtherType_dict.ranged_ethertypes.get(
                            key, "EtherType was not found"
                        )
                    break
        
class arpDesc():
    def __init__(self,arp):
        pass

        