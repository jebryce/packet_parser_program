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
# my_Packet.ARP.opcode                 | returns a bytes object
#                                      | ex: 01 (type: bytes)
# my_Packet.ARP.desc.opcode            | returns a string that describes
#                                      | ex: 'Request' (type: string)
# generally:                           |
# my_Packet.variable                   | calls the data of variable
# my_Packet.desc.variable              | calls the description of variable
# 
from johnParser.functions import sdnParserDescriptions

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
            # 8100 (type: bytes)
            self.tagged = packet[12:14]

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

        self.partial_packet = partialPacket[2:]


        # I couldn't think of a better way to do this (that was as readable)
        # this creates a new class object that then parsers the rest of the 
        # packet. If nothing is found, the variables 
        # self.ethertype and self.ethertype_desc (should) always have values  
        self.desc = sdnParserDescriptions.Packet_desc(self)
        if self.ethertype.hex() == '0806':
            self.ARP = ARP(self)
        elif self.ethertype.hex() == '0800':
            self.IPv4 = IPv4(self)
            # self.ipv4 = ipv4(partialPacket[2:])
        # see sdnParserDescriptions for more detail, but it creates 
        # descriptions for a self.variable at self.desc.variable 
        self.desc.finish_descriptions(self)





class ARP:
    def __init__(self, Packet):
        # Decided to chop off the front of the packet as tagged traffic would 
        # have different index values

        # ex: 0001 (type: bytes)
        self.hardware_type = Packet.partial_packet[0:2]

        # this shares the same EtherType numbers/descriptions
        # ex: 0800 (type: bytes)
        self.protocol_type = Packet.partial_packet[2:4]

        # index [4:5] returns a bytes object, index[5] returns an integer
        # ex: 06 (type: bytes)
        self.hardware_size = Packet.partial_packet[4:5]

        # ex: 04 (type: bytes)
        self.protocol_size = Packet.partial_packet[5:6]

        # ex: 0001 (type: bytes)
        self.opcode = Packet.partial_packet[6:8]

        # ex: B8 27 EB 3C 2D 60 (type: bytes)
        self.sender_mac_address = Packet.partial_packet[8:14]

        # ex: A9 FE B2 34 (type: bytes)
        self.sender_ip_address = Packet.partial_packet[14:18]

        # ex: 00 00 00 00 00 00 (type: bytes)
        self.target_mac_address = Packet.partial_packet[18:24]

        # ex: 80 AB 01 01 (type: bytes)     
        self.target_ip_address = Packet.partial_packet[24:28]

        self.desc = sdnParserDescriptions.ARP_desc(self, Packet)


class IPv4:
    def __init__(self, Packet):
        self.version = (Packet.partial_packet[0] >> 4).to_bytes(1,'big')
        self.ihl = (Packet.partial_packet[0] & 0b1111).to_bytes(1,'big')
        self.dscp = (Packet.partial_packet[1] >> 2).to_bytes(2,'big')
        self.ecn = (Packet.partial_packet[1] & 0b11).to_bytes(1,'big')

        self.total_length = Packet.partial_packet[2:4]
        self.identification = Packet.partial_packet[4:6]

        self.flags = (Packet.partial_packet[6] >> 5).to_bytes(1,'big')

        self.fragment_offset = Packet.partial_packet[6] & 0b11111 * 256
        self.fragment_offset += Packet.partial_packet[7]
        self.fragment_offset = self.fragment_offset.to_bytes(1,'big')



        self.ttl = Packet.partial_packet[8:9]
        self.protocol = Packet.partial_packet[9:10]
        self.checksum = Packet.partial_packet[10:12]
        self.source_ip_address = Packet.partial_packet[12:16]
        self.destination_ip_address = Packet.partial_packet[16:20]

        self.partial_packet = Packet.partial_packet[20:]
        if self.protocol.hex() == '01':
            self.ICMP = ICMP(self)

class ICMP:
    def __init__(self, IPv4):
        self.type = IPv4.partial_packet[0:1]
        self.code = IPv4.partial_packet[1:2]
        self.checksum = IPv4.partial_packet[2:4]
        self.identifier = IPv4.partial_packet[4:6]
        self.sequence_number = IPv4.partial_packet[6:8]

