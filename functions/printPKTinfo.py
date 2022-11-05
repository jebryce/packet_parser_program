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



    
    # Print MAC address info
    pf.print_bar()
    pf.print_data(
        column_widths=[15,30]
        type = 'Type', data = 'MAC Address', desc='Vendor ID'
    )
    pf.print_address(type = 'Type', data = 'MAC Address', desc='Vendor ID')
    pf.print_address_line()
    pf.print_address(
        type = 'Source', 
        data = Packet.source_mac_address.hex(':').upper(), 
        desc = Packet.desc.source_mac_address
    )
    pf.print_address(
        type = 'Destination', 
        data = Packet.destination_mac_address.hex(':').upper(), 
        desc = Packet.desc.destination_mac_address
    )

    
    # Print EtherType info
    pf.print_bar()
    pf.print_info(
        type = 'EtherType', 
        data = 'Value (numbers are in hex)', 
        desc = 'Description'
    )
    pf.print_info_line()

    # Print if tagged traffic
    if Packet.tagged == True:
        pf.print_info(type = '802.1Q', data = '8100', desc = Packet.desc.tagged)
        pf.print_info_data(
            type = 'VLAN ID',
            data = Packet.vlan_id.hex().upper().lstrip('0'), 
            desc = Packet.desc.vlan_id
        )
        pf.print_info_line()

    # Print if ARP packet
    if Packet.ethertype.hex() == '0806':
        # Print ARP stuff
        pf.print_info(type = 'ARP', data = '0806', desc = Packet.desc.ethertype)
        pf.print_info_data( 
            type = 'Hardware Type',
            data = Packet.arp.hardware_type.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.hardware_type
        )
        pf.print_info_data(
            type = 'Protocol Type', 
            data = Packet.arp.protocol_type.hex().upper(), 
            desc = Packet.arp.desc.protocol_type
        )
        pf.print_info_data(
            type = 'Hardware Size', 
            data = Packet.arp.hardware_size.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.hardware_size
        )
        pf.print_info_data(
            type = 'Protocol Size', 
            data = Packet.arp.protocol_size.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.protocol_size
        )
        pf.print_info_data(
            type = 'Opcode', 
            data = Packet.arp.opcode.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.opcode
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
    
