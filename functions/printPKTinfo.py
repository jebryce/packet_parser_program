# Given a packet we want first parse the packet, but since the parsed 
# information will be used later, we want a seperate function to print that 
# information. 
#
# This file contains the function 'createPrintList', which generates a list of 
# strings to be printed. Which then are printed by the 'printPKTinfo' function
#
# I decided to do it this way, as in the future I would like functionality to 
# print to either the console or a text file (or both!).
#
from functions import print_functions





def printPKTinfo(Packet, console = True, file_path=None, bar_length=150):
    # Packet variable is an object of Packet class defined 
    # in /functions/sdnParser.py

    # see /functions/print_functions.py for more info. It is just a class that 
    # contains functions that format and print a string to console.
    pf = print_functions.print_functions(console, file_path, bar_length)

    # Honestly am surprised this worked
    # this is convert a 4-octet ip address (in type bytes)
    # to a human-readable ip address in the format int.int.int.int
    bytes2ip = '{}.{}.{}.{}'
    # example: bytes2ip.format(*variable)
    # need the asterisk, where variable is a 4-octect bytes object

    # these determine the widths of the first two columns for each data type
    mac_width = [11, 17]
    arp_width = [13, 26]

    
    # Print MAC address info
    pf.print_bar()
    pf.print_data(
        column_widths = mac_width,
        entries = ['Type', 'MAC Address', 'Vendor ID'],
        just = '^'
    )
    pf.print_data_bar(column_widths = mac_width)
    pf.print_data(
        column_widths = mac_width,
        entries = [
            'Source',
            Packet.source_mac_address.hex(':').upper(), 
            Packet.desc.source_mac_address
        ],
        just = '^'
    )
    pf.print_data(
        column_widths = mac_width,
        entries = [
            'Destination',
            Packet.destination_mac_address.hex(':').upper(), 
            Packet.desc.destination_mac_address
        ],
        just = '^'
    )


    # Print EtherType info
    pf.print_bar()
    pf.print_data(
        column_widths=arp_width,
        entries=['EtherType', 'Value (hex)', 'Description']
    )
    pf.print_data_bar(column_widths = arp_width)

    # Print if tagged traffic
    if Packet.tagged != False:
        pf.print_data(
            column_widths = arp_width,
            entries = ['802.1Q', '8100', Packet.desc.tagged]
        )
        pf.print_data(
            column_widths = arp_width,
            entries = [
                'VLAN ID', 
                Packet.vlan_id.hex().upper().lstrip('0'),
                Packet.desc.vlan_id
            ],
            arrow_length = 3
        )
        pf.print_data_bar(column_widths = arp_width)

    # Print if ARP packet
    if Packet.ethertype.hex() == '0806':
        # Print ARP stuff
        pf.print_data(
            column_widths = arp_width,
            entries = ['ARP', '0806', Packet.desc.ethertype]
        )

        pf.print_data( 
            column_widths = arp_width,
            entries = [
                'Hardware Type',
                Packet.arp.hardware_type.hex().upper().lstrip('0'), 
                Packet.arp.desc.hardware_type
            ],
            arrow_length = 3
        )
        pf.print_data( 
            column_widths = arp_width,
            entries = [
                'Protocol Type',
                Packet.arp.protocol_type.hex().upper(), 
                Packet.arp.desc.protocol_type
            ],
            arrow_length = 3
        )
        pf.print_data( 
            column_widths = arp_width,
            entries = [
                'Hardware Size',
                Packet.arp.hardware_size.hex().upper().lstrip('0'), 
                Packet.arp.desc.hardware_size
            ],
            arrow_length = 3
        )
        pf.print_data( 
            column_widths = arp_width,
            entries = [
                'Protocol Size',
                Packet.arp.protocol_size.hex().upper().lstrip('0'), 
                Packet.arp.desc.protocol_size
            ],
            arrow_length = 3
        )
        pf.print_data( 
            column_widths = arp_width,
            entries = [
                'Opcode',
                Packet.arp.opcode.hex().upper().lstrip('0'), 
                Packet.arp.desc.opcode
            ],
            arrow_length = 3
        )
        
        
        # ARP provides MAC address as well, but it is different when 
        # Opcode = 1 (request)
        pf.print_bar()
        pf.print_address(
            type = 'Type', 
            data = 'Hardware Address', 
            desc='Vendor ID'
        )
        pf.print_address_line()
        pf.print_address(
            type = 'ARP Sender', 
            data = Packet.arp.sender_mac_address.hex(':').upper(), 
            desc = Packet.arp.desc.sender_mac_address
        )
        pf.print_address(
            type = 'ARP Target', 
            data = Packet.arp.target_mac_address.hex(':').upper(), 
            desc = Packet.arp.desc.target_mac_address
        )
        pf.print_address_line()

        # IP address
        pf.print_address(
            type = 'Type', 
            data = 'Protocol Address', 
            desc='Location'
        )
        pf.print_address_line()
        pf.print_address(
            type = 'ARP Sender', 
            data = bytes2ip.format(*Packet.arp.sender_ip_address), 
            desc = Packet.arp.desc.sender_ip_address
        )
        pf.print_address(
            type = 'ARP Target', 
            data = bytes2ip.format(*Packet.arp.target_ip_address), 
            desc = Packet.arp.desc.target_ip_address
        )


    pf.print_bar()
    
