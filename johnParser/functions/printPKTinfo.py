# Given a packet we want first parse the packet, but since the parsed 
# information will be used later, we want a seperate function to print that 
# information. 
# 
# This file contains classes that print the parsed data. 
# 
from johnParser.functions import print_functions

class print_packet_info():
    def __init__(
        self, Packet, console = True, file_path = None, bar_length = 150
    ):
        # Packet variable is an object of Packet class defined 
        # in /functions/sdnParser.py
        # (this is the parsed data)
        self.Packet = Packet

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
            print_arp_info(self)
        
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

        # Auto fit first column's length to longest title
        title_length = max(len(source_title),len(dest_title))
        mac_widths = [title_length, 17]

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
        
        # Auto fit first column's length to longest title
        title_length = max(len(source_title),len(dest_title))
        ipv4_widths = [title_length, 17]

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

    def print_ethertype(self, column_widths, ethertype_abbreviation):
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
            column_widths=column_widths,
            entries=['EtherType', 'Value (hex)', 'Description']
        )
        self.pf.print_data_bar(column_widths = column_widths)

        # Print if tagged traffic
        if self.Packet.tagged != False:
            self.pf.print_data(
                column_widths = column_widths,
                entries = ['802.1Q', '8100', self.Packet.desc.tagged]
            )
            self.pf.print_data(
                column_widths = column_widths,
                entries = [
                    'VLAN ID', 
                    self.Packet.vlan_id.hex().upper(),
                    self.Packet.desc.vlan_id
                ],
                arrow_length = 3
            )
            self.pf.print_data_bar(column_widths = column_widths)

        # print the ethertype of the packet
        self.pf.print_data(
            column_widths = column_widths,
            entries = [
                ethertype_abbreviation,
                self.Packet.ethertype.hex().upper(), 
                self.Packet.desc.ethertype
                ]
        )
        
class print_arp_info(print_packet_info):
    def __init__(self, parent):
        # widths of the first 2 columns 
        self.arp_widths = [9, 22]
        # then we just print the data of the packet

        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #  EtherType | Value (hex)            | Description 
        # -----------+------------------------+---------------------------------
        #     802.1Q | 8100                   | Customer VLAN Tagged Type 
        #            |--> VLAN ID: 0003       | SDN Production VLAN 
        # -----------+------------------------+---------------------------------
        #        ARP | 0806                   | Address Resolution Protocol
        parent.print_ethertype(self.arp_widths,'ARP')

        # ex: (note descriptions were cut off)
        #            |--> Hardware Type: 1    | placeholder for lookup
        #            |--> Protocol Type: 0800 | IPv4 
        #            |--> Hardware Size: 6    | Length of the hardware address
        #            |--> Protocol Size: 4    | Length of the protocol address
        #            |--> Opcode: 1           | placeholder for opcode lookup 
        self.print_arp_data(parent)

        # ex: 
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #       Type |    MAC Address    | Vendor ID 
        # -----------+-------------------+-------------------------------------
        # ARP Sender | B8:27:EB:3C:2D:60 | Raspberry Pi Foundation 
        # ARP Target | 00:00:00:00:00:00 | Target not yet known
        parent.print_mac_address_table(
            'ARP Sender',
            parent.Packet.arp.sender_mac_address,
            parent.Packet.arp.desc.sender_mac_address,
            'ARP Target',
            parent.Packet.arp.target_mac_address,
            parent.Packet.arp.desc.target_mac_address
        )

        # ex:
        #% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #        Type |   IPv4 Address    | Location 
        # ------------+-------------------+-------------------------------------
        #  ARP Sender |  169.254.178.52   | placeholder for IP lookup 
        #  ARP Target |    128.171.1.1    | placeholder for IP lookup 
        parent.print_ipv4_address_table(
            'ARP Sender',
            parent.Packet.arp.sender_ip_address,
            parent.Packet.arp.desc.sender_ip_address,
            'ARP Target',
            parent.Packet.arp.target_ip_address,
            parent.Packet.arp.desc.target_ip_address, 
        )

    def print_arp_data(self,parent):
        # this goes through and prints each line of data associated with an arp 
        # packet. I decided to make this a seperate function as to make the 
        # flow of the printing more clear.

        # print hardware type
        parent.pf.print_data( 
            column_widths = self.arp_widths,
            entries = [
                'Hardware Type',
                parent.Packet.arp.hardware_type.hex().upper().lstrip('0'), 
                parent.Packet.arp.desc.hardware_type
            ],
            arrow_length = 3
        )
        # print protocol type
        parent.pf.print_data( 
            column_widths = self.arp_widths,
            entries = [
                'Protocol Type',
                parent.Packet.arp.protocol_type.hex().upper(), 
                parent.Packet.arp.desc.protocol_type
            ],
            arrow_length = 3
        )
        # print hardware size
        parent.pf.print_data( 
            column_widths = self.arp_widths,
            entries = [
                'Hardware Size',
                parent.Packet.arp.hardware_size.hex().upper().lstrip('0'), 
                parent.Packet.arp.desc.hardware_size
            ],
            arrow_length = 3
        )
        # print protocol size
        parent.pf.print_data( 
            column_widths = self.arp_widths,
            entries = [
                'Protocol Size',
                parent.Packet.arp.protocol_size.hex().upper().lstrip('0'), 
                parent.Packet.arp.desc.protocol_size
            ],
            arrow_length = 3
        )
        # print opcode
        parent.pf.print_data( 
            column_widths = self.arp_widths,
            entries = [
                'Opcode',
                parent.Packet.arp.opcode.hex().upper().lstrip('0'), 
                parent.Packet.arp.desc.opcode
            ],
            arrow_length = 3
        )





