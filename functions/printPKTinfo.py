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
import hexdump
import os
def createPrintList(Packet):
    # Packet variable is an object of Packet class defined 
    # in /functions/sdnParser.py

    # This function populates a list full of strings
    printList = []

    # bar_length is the number of characters wide to print the table row borders
    bar_length = 100

    # Initialize string formats
    # I created this functions, as it imo it is more readable to code
    # print_address() instead of printList.append(pkt_address_table.format()) 

    # ex: '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
    def print_bar():
        bar = bar_length*'%'
        return printList.append(bar)

    # ex: '         Type |    MAC Address    | Vendor ID'
    def print_address(type = None, data = None, desc = None):
        pkt_address_table = "  {type:>11} | {data:^17} | {desc}"
        return printList.append(pkt_address_table.format(
                type = type, data = data, desc = desc
            ))
    
    # ex: '--------------+-------------------+---------------------------------'
    def print_address_line():
        address_line = 14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-'
        return printList.append(address_line)

    # ex: '    EtherType | Value (numbers are in hex)     | Description'
    def print_info(type = None, data = None, desc = None):
        pkt_info_table = "  {type:>11} | {data:<30} | {desc}"
        return printList.append(pkt_info_table.format(
                type = type, data = data, desc = desc
            ))
        
    # ex: '              |--> VLAN ID: 3                  | SDN Production VLAN'
    def print_info_data(type = None, data = None, desc = None):
        type_data = type+': '+ data
        pkt_info_data_table = 14*' '+"|--> {type_data:<27} | {desc}"
        return printList.append(pkt_info_data_table.format(
               type_data = type_data, desc = desc
            ))

    # ex: '--------------+--------------------------------+--------------------'
    def print_info_line():
        info_line = 14*'-'+'+'+32*'-'+'+'+(bar_length-48)*'-'
        return printList.append(info_line)

    # Honestly am surprised this worked
    bytes2ip = '{}.{}.{}.{}'
    # example: bytes2ip.format(*variable)
    # need the asterisk



    
    # Print MAC address info
    print_bar()
    print_address(type = 'Type', data = 'MAC Address', desc='Vendor ID')
    print_address_line()
    print_address(
        type = 'Source', 
        data = Packet.source_mac_address.hex(':').upper(), 
        desc = Packet.desc.source_mac_address
    )
    print_address(
        type = 'Destination', 
        data = Packet.destination_mac_address.hex(':').upper(), 
        desc = Packet.desc.destination_mac_address
    )

    
    # Print EtherType info
    print_bar()
    print_info(
        type = 'EtherType', 
        data = 'Value (numbers are in hex)', 
        desc = 'Description'
    )
    print_info_line()

    # Print if tagged traffic
    if Packet.tagged == True:
        print_info(type = '802.1Q', data = '8100', desc = Packet.desc.tagged)
        print_info_data(
            type = 'VLAN ID',
            data = Packet.vlan_id.hex().upper().lstrip('0'), 
            desc = Packet.desc.vlan_id
        )
        print_info_line()

    # Print if ARP packet
    if Packet.ethertype.hex() == '0806':
        # Print ARP stuff
        print_info(type = 'ARP', data = '0806', desc = Packet.desc.ethertype)
        print_info_data( 
            type = 'Hardware Type',
            data = Packet.arp.hardware_type.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.hardware_type
        )
        print_info_data(
            type = 'Protocol Type', 
            data = Packet.arp.protocol_type.hex().upper(), 
            desc = Packet.arp.desc.protocol_type
        )
        print_info_data(
            type = 'Hardware Size', 
            data = Packet.arp.hardware_size.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.hardware_size
        )
        print_info_data(
            type = 'Protocol Size', 
            data = Packet.arp.protocol_size.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.protocol_size
        )
        print_info_data(
            type = 'Opcode', 
            data = Packet.arp.opcode.hex().upper().lstrip('0'), 
            desc = Packet.arp.desc.opcode
        )
        
        # ARP provides MAC address as well, but it is different when 
        # Opcode = 1 (request)
        print_bar()
        print_address(type = 'Type', data = 'Hardware Address', desc='Vendor ID')
        print_address_line()
        print_address(
            type = 'ARP Sender', 
            data = Packet.arp.sender_mac_address.hex(':').upper(), 
            desc = Packet.arp.desc.sender_mac_address
        )
        print_address(
            type = 'ARP Target', 
            data = Packet.arp.target_mac_address.hex(':').upper(), 
            desc = Packet.arp.desc.target_mac_address
        )
        print_address_line()

        # IP address
        print_address(type = 'Type', data = 'Protocol Address', desc='Location')
        print_address_line()
        print_address(
            type = 'ARP Sender', 
            data = bytes2ip.format(*Packet.arp.sender_ip_address), 
            desc = Packet.arp.desc.sender_ip_address
        )
        print_address(
            type = 'ARP Target', 
            data = bytes2ip.format(*Packet.arp.target_ip_address), 
            desc = Packet.arp.desc.target_ip_address
        )


    print_bar()
    return printList
    

def printPKTinfo(Packet):
    printList = createPrintList(Packet)

    #os.system('cls')
    
    for line in printList:
        print(line)

    hexdump.hexdump(Packet.packet)


