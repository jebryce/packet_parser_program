import EtherType_dict

class Packet:
    def __init__(self, packet):
        # packet is a bytes object
        self.packet = packet

        # ex: b'\xff\xff\xff\xff\xff\xff' (type: bytes)
        # in hex this would be: FF:FF:FF:FF:FF:FF
        self.destination_mac_address = packet[0:6]
        self.source_mac_address = packet[6:12]

        # Check if tagged traffic 
        # 8100 is the EtherType 802.1Q (aka tagged traffic)
        if packet[12:14].hex()=='8100':
            # Decided to use a boolean variable as it is either tagged or not 
            self.tagged = True

            # ex: 0003 (type: bytes)
            self.vlan_id = packet[14:16]

            # the rest of the packet, this is to avoid a seperate variable to 
            # keep track of the differing index due to the 802.1Q header
            etherTypePacket = packet[16:]
        else:
            self.tagged = False
            etherTypePacket = packet[12:]


        self.findEtherType(etherTypePacket)


    def findEtherType(self, partialPacket):
        # decided to make this a seperate function in case we get a packet with 
        # an Ether Type I haven't made a class for yet

        # ex: 0806 (type: bytes)
        self.ethertype = partialPacket[0:2]

        # looks up ethertype value in dictionary to find description
        # ex: 'Address Resolution Protocol (ARP)' (type: string)
        self.ethertype_desc = EtherType_dict.ethertypes.get(
            self.ethertype.hex()
        )                                            
        # if the key in dictionary.get(key) does not exist, it returns None


        # this will probably never get called, but essentially does the same as 
        # previous method, but for rarer ranged ethertypes.
        if self.ethertype_desc == None:
            for key in EtherType_dict.ranged_ethertypes:

                # if the upper value of the range is greater than the ethertype
                # this works as the dictionary is in incremental order
                if bytes.fromhex(key[5:]) >= self.ethertype:

                    # \ character indicates expression is on next line
                    self.ethertype_desc = \
                        EtherType_dict.ranged_ethertypes.get(key)
                    break
            
    
        # will replace laters
        if self.ethertype.hex() == '0806':
            self.arp = arp(partialPacket[2:])
        elif self.ethertype.hex() == '0800':
            self.ipv4 = ipv4(partialPacket[2:])

class arp(Packet):
    def __init__(self, arp_packet):
        # Decided to chop off the front of the packet as tagged traffic would have different index values
        self.arp_packet = arp_packet

        self.hardware_type = self.arp_packet[0:2]
        self.protocol_type = self.arp_packet[2:4]

        # index [4:5] returns a bytes object, index[5] returns an integer
        self.hardware_size = self.arp_packet[4:5]
        self.protocol_size = self.arp_packet[5:6]

        self.opcode = self.arp_packet[6:8]

        self.sender_mac_address = self.arp_packet[8:14]
        self.sender_ip_address = self.arp_packet[14:18]

        self.target_mac_address = self.arp_packet[18:24]
        self.target_ip_address = self.arp_packet[24:28]

class ipv4(Packet):
    pass
