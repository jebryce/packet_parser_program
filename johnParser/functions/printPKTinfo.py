# Given a packet we want first parse the packet, but since the parsed 
# information will be used later, we want a seperate function to print that 
# information. 
# 
# This file contains classes that print the parsed data. 
# 
from johnParser.functions import print_functions, john_hexdump

class print_packet_info():
    def __init__(
        self, Packet, console = True, file_path = None, bar_length = 150
    ):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py
        # (this is the parsed data)
        self.Packet = Packet

        self.widths = Packet.print_widths

        # see /functions/print_functions.py for more info. It is just a class 
        # that contains functions that format and print a string to either the 
        # console, a file, or both.
        self.pf = print_functions.print_functions(
            console, file_path, bar_length
        )

        # first print the ethernet frames mac addresses
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |    MAC Address    | Vendor ID 
        # ------------+-------------------+-------------------------------------
        #      Source | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # Destination | FF:FF:FF:FF:FF:FF | Broadcast 
        self.print_mac_address_table(
            'Source', 
            Packet.source_mac_address, 
            Packet.desc.source_mac_address, 
            'Destination',
            Packet.destination_mac_address, 
            Packet.desc.destination_mac_address
        )
        # then allow the subclasses to print everything else
        # I did this as it is easier to size the columns minimally
        if Packet.ethertype.hex() == '0806':
            print_ARP_info(self)
        elif Packet.ethertype.hex() == '0800':
            print_IPv4_info(self)

        # 139 is the length of a line in the hexdump if 32 bytes per line
        if bar_length >= 139:
            bytes_per_line = 32
        elif bar_length >= 73:
            bytes_per_line = 16
        else:
            bytes_per_line = 8

        hexdump = john_hexdump.john_hexdump(self.Packet.packet, bytes_per_line)
        self.pf.print_bar()
        self.pf.optional_print(hexdump)
        
    def print_mac_address_table(
       self, source_title, source_mac, source_mac_desc,
       dest_title, dest_mac, dest_mac_desc
    ):
        # from the example below, source_title = 'Source' (type: string)
        # source_mac_address = bB27EB3C2D60 (type: bytes)
        # source_mac_desc = 'Raspberry Pi Foundation' (type: string)
        # dest(ination) variables are similar
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |    MAC Address    | Vendor ID 
        # ------------+-------------------+-------------------------------------
        #      Source | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # Destination | FF:FF:FF:FF:FF:FF | Broadcast 

        mac_widths = [11, 17]

        # Print the table as shown above, each self.pf.print_x call prints a row
        # print mac address column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths = mac_widths,
            entries = ['Type', 'MAC Address', 'Vendor ID'],
            just = '^'
        )
        self.pf.print_data_bar(column_widths = mac_widths)
        # print source mac address
        self.pf.print_data(
            column_widths = mac_widths,
            entries = [
                source_title,
                source_mac.hex(':').upper(), 
                source_mac_desc
            ],
            just = '^'
        )
        # print destination mac address
        self.pf.print_data(
            column_widths = mac_widths,
            entries = [
                dest_title,
                dest_mac.hex(':').upper(), 
                dest_mac_desc
            ],
            just = '^'
        )
        
    def print_ipv4_address_table(
        self, source_title, source_ipv4, source_ipv4_desc, 
        dest_title, dest_ipv4, dest_ipv4_desc
    ):
        # from the example below, source_title = 'Source' (type: string)
        # source_ipv4_address = bA9FEB234 (type: bytes)
        # source_ipv4_desc = 'placeholder for IP lookup' (type: string)
        # dest(ination) variables are similar
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |   IPv4 Address    | Location 
        # ------------+-------------------+-------------------------------------
        #  ARP Sender |  169.254.178.52   | placeholder for IP lookup 
        #  ARP Target |    128.171.1.1    | placeholder for IP lookup 
        
        ipv4_widths = [11, 17]

        # Honestly am surprised this worked
        # this is convert a 4-octet ipv4 address (in type bytes)
        # to a human-readable ip address in the format int.int.int.int
        bytes2ip = '{}.{}.{}.{}'
        # example: bytes2ip.format(*variable)
        # need the asterisk (the unpacking operator), where variable is a 
        # 4-octet bytes object
    
        # Print the table as shown above, each self.pf.print_x call prints a row
        # print ipv4 column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = ['Type', 'IPv4 Address', 'Location'],
            just = '^'
        )
        self.pf.print_data_bar(column_widths = ipv4_widths)
        # print source ipv4 address
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = [
                source_title,
                bytes2ip.format(*source_ipv4), 
                source_ipv4_desc
            ],
            just = '^'
        )
        # print destination ipv4 address
        self.pf.print_data(
            column_widths = ipv4_widths,
            entries = [
                dest_title,
                bytes2ip.format(*dest_ipv4), 
                dest_ipv4_desc
            ],
            just = '^'
        )

    def print_ethertype(self, ethertype_abbreviation):
        # from the example below, column_widths is a list of two integers that 
        # determine the widths of the first two columns. In this example it is 
        # [9, 22] (type: list of two integers)
        # ethertype_abbreviation = 'ARP' (type: string)
        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #  EtherType | Value (hex)            | Description 
        # -----------+------------------------+---------------------------------
        #     802.1Q | 8100                   | Customer VLAN Tagged Type 
        #            |--> VLAN ID: 0003       | SDN Production VLAN 
        # -----------+------------------------+---------------------------------
        #        ARP | 0806                   | Address Resolution Protocol


        # Print EtherType column headers
        self.pf.print_bar()
        self.pf.print_data(
            column_widths=self.widths,
            entries=['Protocol', 'Value (hex)', 'Description']
        )
        self.pf.print_data_bar(column_widths = self.widths)

        # Print if tagged traffic
        if self.Packet.tagged != False:
            self.pf.print_data(
                column_widths = self.widths,
                entries = ['802.1Q', '8100', self.Packet.desc.tagged]
            )
            self.pf.print_data(
                column_widths = self.widths,
                entries = [
                    'VLAN ID', 
                    self.Packet.vlan_id.hex().upper(),
                    self.Packet.desc.vlan_id
                ],
                arrow_length = 3
            )
            self.pf.print_data_bar(column_widths = self.widths)

        # print the ethertype of the packet
        self.pf.print_data(
            column_widths = self.widths,
            entries = [
                ethertype_abbreviation,
                self.Packet.ethertype.hex().upper(), 
                self.Packet.desc.ethertype
                ]
        )
        
class print_ARP_info(print_packet_info):
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
        self.print_ARP_data(parent)


    def print_ARP_data(self, parent):
        # this goes through and prints each line of data associated with an ARP 
        # packet. I decided to make this a seperate function as to make the 
        # flow of the printing more clear.

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

class print_IPv4_info(print_packet_info):
    def __init__(self, parent):
        parent.print_ipv4_address_table(
            'Source',
            parent.Packet.IPv4.source_ip_address,
            parent.Packet.IPv4.desc.source_ip_address,
            'Destination',
            parent.Packet.IPv4.destination_ip_address,
            parent.Packet.IPv4.desc.destination_ip_address
        )

        parent.print_ethertype('IPv4')

        self.print_ipv4_data(parent)

        if parent.Packet.IPv4.protocol.hex() == '01':
            print_ICMP_info(parent)
        elif parent.Packet.IPv4.protocol.hex() == '11':
            print_UDP_info(parent)

    def print_ipv4_data(self, parent):
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Version',
                parent.Packet.IPv4.version.hex().upper(), 
                parent.Packet.IPv4.desc.version
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Header Length',
                parent.Packet.IPv4.ihl.hex().upper(), 
                parent.Packet.IPv4.desc.ihl
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'DSCP',
                parent.Packet.IPv4.dscp.hex().upper(), 
                parent.Packet.IPv4.desc.dscp
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'ECN',
                parent.Packet.IPv4.ecn.hex().upper(), 
                parent.Packet.IPv4.desc.ecn
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Total Length',
                parent.Packet.IPv4.total_length.hex().upper(), 
                parent.Packet.IPv4.desc.total_length
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Identification',
                parent.Packet.IPv4.identification.hex().upper(), 
                parent.Packet.IPv4.desc.identification
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flags',
                parent.Packet.IPv4.flags.hex().upper(), 
                parent.Packet.IPv4.desc.flags
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Fragment Offset',
                parent.Packet.IPv4.fragment_offset.hex().upper(), 
                parent.Packet.IPv4.desc.fragment_offset
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Time to Live',
                parent.Packet.IPv4.ttl.hex().upper(), 
                parent.Packet.IPv4.desc.ttl
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Protocol',
                parent.Packet.IPv4.protocol.hex().upper(), 
                parent.Packet.IPv4.desc.protocol
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.checksum.hex().upper(), 
                parent.Packet.IPv4.desc.checksum
            ],
            arrow_length = 3
        )

class print_ICMP_info(print_packet_info):
    def __init__(self, parent):  
        parent.pf.print_data_bar(parent.widths)
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'ICMP',
                '01', 
                'Internet Control Message Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Type',
                parent.Packet.IPv4.ICMP.type.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.type
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Code',
                parent.Packet.IPv4.ICMP.code.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.code
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.ICMP.checksum.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.checksum
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Identifier',
                parent.Packet.IPv4.ICMP.identifier.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.identifier
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                parent.Packet.IPv4.ICMP.sequence_number.hex().upper(), 
                parent.Packet.IPv4.ICMP.desc.sequence_number
            ],
            arrow_length = 3
        )

class print_UDP_info(print_packet_info):
    def __init__(self, parent):

        parent.pf.print_data_bar(parent.widths)
        self.print_UDP_data(parent)

        # port 6343 dec = 18c7 hex
        if parent.Packet.IPv4.UDP.destination_port.hex() == '18c7': 
            print_sFlow_info(parent)


    def print_UDP_data(self, parent):
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'UDP',
                '11', 
                'User Datagram Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source Port',
                parent.Packet.IPv4.UDP.source_port.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.source_port
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Destination Port',
                parent.Packet.IPv4.UDP.destination_port.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.destination_port
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Length',
                parent.Packet.IPv4.UDP.length.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.length
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.UDP.checksum.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.checksum
            ],
            arrow_length = 3
        )

class print_sFlow_info(print_packet_info):
    def __init__(self, parent):
        # so I wouldn't have to type out (or copy) this long ass message
        sFlow = parent.Packet.IPv4.UDP.sFlow

        parent.pf.print_data_bar(parent.widths)
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'sFlow',
                '18C7', 
                'InMon sFlow (sampled flow) Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Version',
                sFlow.datagram_version.hex().upper(), 
                sFlow.desc.datagram_version
            ],
            arrow_length = 3
        )  
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Address Type',
                sFlow.agent_address_type.hex().upper(), 
                sFlow.desc.agent_address_type
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Agent Address',
                '{}.{}.{}.{}'.format(*sFlow.agent_address),
                sFlow.desc.agent_address
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sub-agent ID',
                sFlow.sub_agent_id.hex().upper(), 
                sFlow.desc.sub_agent_id
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sequence Number',
                sFlow.sequence_number.hex().upper(), 
                sFlow.desc.sequence_number
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'System Uptime',
                sFlow.system_uptime.hex().upper(), 
                sFlow.desc.system_uptime
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Sample Count',
                sFlow.number_of_samples.hex().upper(), 
                sFlow.desc.number_of_samples
            ],
            arrow_length = 3
        )






