from johnParser.functions.path import PATH
from johnParser.protocols import Ethernet

class ARP():
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

class ARP_desc():
    def __init__(self, Packet):
        # lookup hardware type description
        self.hardware_type = self.hardware_type_lookup(
            Packet.ARP.hardware_type
        )

        # this shares the same EtherType numbers/descriptions
        # so lookup all ethertype descriptions
        ethertypes = Packet.desc.ethertype_lookup(
            Packet.ARP.protocol_type,
            Packet.ethertype
        )
        # then assign them to the correct variables
        self.protocol_type = ethertypes[Packet.ARP.protocol_type]
        Packet.desc.protocol_type = ethertypes[Packet.ethertype]

        self.hardware_size = 'Length of the hardware (MAC) address.'

        self.protocol_size = 'Length of the network protocol (IPv4) address.'

        # lookup opcode description
        self.opcode = self.opcode_lookup(Packet.ARP.opcode)

        # lookup mac addresses vendor ids
        mac_addresses = Packet.desc.mac_address_lookup(
            Packet.source_mac_address,
            Packet.destination_mac_address,
            Packet.ARP.sender_mac_address,
            Packet.ARP.target_mac_address
        )
        # then assign them to the correct variables
        Packet.desc.source_mac_address = \
            mac_addresses[Packet.source_mac_address]
        Packet.desc.destination_mac_address = \
            mac_addresses[Packet.destination_mac_address]
        self.sender_mac_address = mac_addresses[Packet.ARP.sender_mac_address]
        self.target_mac_address = mac_addresses[Packet.ARP.target_mac_address]

        # TODO implement ip address lookup
        self.sender_ip_address = 'Placeholder for IPv4 address lookup.'
        self.target_ip_address = 'Placeholder for IPv4 address lookup.'

    def opcode_lookup(self, opcode):
        # takes in an ARP opcode, returns it's description

        # 'with' statement closes the file after we are finished with it
        opcode_file = PATH + 'ARP_opcode_lookup.txt'
        with open(opcode_file, 'r', encoding='utf-8') as opcode_lookup:
            # skip the first two lines as they are:
            # '# Created using johnParser/functions/make_lookups.py'
            # and
            # 'Number Operation Code (op)'
            opcode_lookup.__next__()
            opcode_lookup.__next__()
            
            # default description
            opcode_desc = 'Unassigned'

            # we look through the file and try to reassign the variable
            for row in opcode_lookup:
                # splits each row into a list of two values, first value is
                # the opcode, and the second vlaue is the description
                # ex: (type: list) ['1', 'REQUEST\n']
                row = row.split(' ', 1)
                if int.from_bytes(opcode,'big') == int(row[0]):
                    opcode_desc = row[1].replace('\n', '').capitalize()
        return opcode_desc

    def hardware_type_lookup(self, hardware_type):
        hardware_type_file = PATH + 'ARP_hardware_lookup.txt'
        with open(hardware_type_file, 'r', encoding='utf-8') as hardware_lookup:
            hardware_lookup.__next__()
            hardware_lookup.__next__()
            hardware_desc = 'Unassigned'
            for row in hardware_lookup:
                row = row.split(' ',1)
                if int.from_bytes(hardware_type,'big') == int(row[0]):
                    hardware_desc = row[1].replace('\n', '')
        return hardware_desc

class print_ARP(Ethernet.print_Ethernet):
    def __init__(self, parent):
        # then we just print the data of the packet

        # ex: 
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #       Type |    MAC Address    | Vendor ID 
        # -----------+-------------------+-------------------------------------
        # ARP Sender | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # ARP Target | 00:00:00:00:00:00 | Target not yet known
        parent.print_mac_address_table(
            'ARP Sender',
            parent.Packet.ARP.sender_mac_address,
            parent.Packet.ARP.desc.sender_mac_address,
            'ARP Target',
            parent.Packet.ARP.target_mac_address,
            parent.Packet.ARP.desc.target_mac_address
        )

        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |   IPv4 Address    | Location 
        # ------------+-------------------+-------------------------------------
        #  ARP Sender |  169.254.178.52   | placeholder for IP lookup 
        #  ARP Target |    128.171.1.1    | placeholder for IP lookup 
        parent.print_ipv4_address_table(
            'ARP Sender',
            parent.Packet.ARP.sender_ip_address,
            parent.Packet.ARP.desc.sender_ip_address,
            'ARP Target',
            parent.Packet.ARP.target_ip_address,
            parent.Packet.ARP.desc.target_ip_address, 
        )

        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #  EtherType | Value (hex)            | Description 
        # -----------+------------------------+---------------------------------
        #     802.1Q | 8100                   | Customer VLAN Tagged Type 
        #            |--> VLAN ID: 0003       | SDN Production VLAN 
        # -----------+------------------------+---------------------------------
        #        ARP | 0806                   | Address Resolution Protocol
        parent.print_ethertype('ARP')

        # ex: (note descriptions were cut off)
        #            |--> Hardware Type: 1    | placeholder for lookup
        #            |--> Protocol Type: 0800 | IPv4 
        #            |--> Hardware Size: 6    | Length of the hardware address
        #            |--> Protocol Size: 4    | Length of the protocol address
        #            |--> Opcode: 1           | placeholder for opcode lookup 

        # print hardware type
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Hardware Type',
                parent.Packet.ARP.hardware_type.hex().upper(), 
                parent.Packet.ARP.desc.hardware_type
            ],
            arrow_length = 3
        )
        # print protocol type
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Protocol Type',
                parent.Packet.ARP.protocol_type.hex().upper(), 
                parent.Packet.ARP.desc.protocol_type
            ],
            arrow_length = 3
        )
        # print hardware size
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Hardware Size',
                parent.Packet.ARP.hardware_size.hex().upper(), 
                parent.Packet.ARP.desc.hardware_size
            ],
            arrow_length = 3
        )
        # print protocol size
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Protocol Size',
                parent.Packet.ARP.protocol_size.hex().upper(), 
                parent.Packet.ARP.desc.protocol_size
            ],
            arrow_length = 3
        )
        # print opcode
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Opcode',
                parent.Packet.ARP.opcode.hex().upper(), 
                parent.Packet.ARP.desc.opcode
            ],
            arrow_length = 3
        )
