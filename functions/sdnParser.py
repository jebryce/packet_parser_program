# Given a packet with type 'bytes', we want to be able to fully parse the 
# packet down to what every byte does. 
#
# This file contains a main class 'Packet' which parsers the very start of the 
# packet (the Ethernet frame) up to the EtherType field. Then the main class 
# creates a subclass for whatever EtherType the packet was, and that subclass 
# continues parsing the packet until a variable is assigned to every byte.
#
# This file also contains all ethertype subclasses the main 'Packet' class 
# creates.
# 
# Also, every class that is defined in this file, has an individual description 
# class created with it, which are defined 
# at /functions/sdnParserDescriptions.py, see for more detail
#
# A way to call the class's variables, for example:
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
from functions import sdnParserDescriptions

class Packet:
    def __init__(self, packet):
        # packet is a bytes object
        self.packet = packet

        # ex: b'\xff\xff\xff\xff\xff\xff' (type: bytes)
        # in hex this would be: FF:FF:FF:FF:FF:FF
        self.destination_mac_address = packet[0:6]
        self.source_mac_address = packet[6:12]

        # Check if tagged traffic, 
        # the .hex() function converts the bytes object to a string of hex 
        # values, 8100 is the EtherType 802.1Q (aka tagged traffic)
        if packet[12:14].hex()=='8100':
            # Decided to use a boolean variable as it is either tagged or not 
            self.tagged = True

            # ex: 0003 (type: bytes)
            self.vlan_id = packet[14:16]

            # the rest of the packet, this is to avoid a seperate variable to 
            # keep track of the differing index due to the 802.1Q header
            partialPacket = packet[16:]
        else:
            self.tagged = False
            partialPacket = packet[12:]

        # ex: 0806 (type: bytes)
        self.ethertype = partialPacket[0:2]


        # I couldn't think of a better way to do this (that was as readable)
        # this creates a new class object that then parsers the rest of the 
        # packet. If nothing is found, the variables 
        # self.ethertype and self.ethertype_desc (should) always have values  
        if self.ethertype.hex() == '0806':
            self.arp = arp(partialPacket[2:])
        elif self.ethertype.hex() == '0800':
            self.ipv4 = ipv4(partialPacket[2:])

        # see sdnParserDescriptions for more detail, but it creates 
        # descriptions for a self.variable at self.desc.variable 
        self.desc = sdnParserDescriptions.PacketDesc(self)



class arp:
    def __init__(self, arp_packet):
        # Decided to chop off the front of the packet as tagged traffic would 
        # have different index values

        # ex: 0001 (type: bytes)
        self.hardware_type = arp_packet[0:2]

        # this shares the same EtherType numbers/descriptions
        # ex: 0800 (type: bytes)
        self.protocol_type = arp_packet[2:4]

        # index [4:5] returns a bytes object, index[5] returns an integer
        # ex: 06 (type: bytes)
        self.hardware_size = arp_packet[4:5]

        # ex: 04 (type: bytes)
        self.protocol_size = arp_packet[5:6]

        # ex: 0001 (type: bytes)
        self.opcode = arp_packet[6:8]

        # ex: B8 27 EB 3C 2D 60 (type: bytes)
        self.sender_mac_address = arp_packet[8:14]

        # ex: A9 FE B2 34 (type: bytes)
        self.sender_ip_address = arp_packet[14:18]

        # ex: 00 00 00 00 00 00 (type: bytes)
        self.target_mac_address = arp_packet[18:24]

        # ex: 80 AB 01 01 (type: bytes)     
        self.target_ip_address = arp_packet[24:28]

        self.desc = sdnParserDescriptions.arpDesc(self)


class ipv4:
    pass
