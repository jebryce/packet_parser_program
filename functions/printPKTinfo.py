import hexdump
import os
def createPrintList(pkt_object):
    # bar_length is the number of characters wide to print the table row borders
    bar_length = 100

    # This function populates a list full of strings
    printList = []

    def print_address(type = None, data = None, desc = None):
        pkt_address_table = "  {type:>11} | {data:^17} | {desc}"
        return printList.append(pkt_address_table.format(
                type = type, data = data, desc = desc
            ))
    
    def print_address_line():
        address_line = 14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-'
        return printList.append(address_line)

    def print_info(type = None, data = None, desc = None):
        pass

    def print_info_line():
        info_line = 14*'-'+'+'+32*'-'+'+'+(bar_length-48)*'-'
        return printList.append(info_line)



    # Initialize string formats
    bar = bar_length*'%'
    

    etherType_table_line = 14*'-'+'+'+32*'-'+'+'+(bar_length-48)*'-'
    etherType_table = "  {type:>11} | {data:<30} | {desc}"
    etherTypedata_table = "  {type:>11} |--> {data:<27} | {desc}"


    # Honestly am surprised this worked
    bytes2ip = '{}.{}.{}.{}'
    # example: bytes2ip.format(*variable)
    # need the asterisk



    # Print MAC address info
    printList.append(bar)
    print_address(type = '', data = 'MAC Address', desc='Vendor ID')
    print_address_line()
    print_address(type = 'Source', data = pkt_object.source_mac_address.hex(':').upper(), desc = '')
    print_address(type = 'Destination', data = pkt_object.destination_mac_address.hex(':').upper(), desc = '')

    
    # Print EtherType info
    printList.append(bar)
    printList.append(etherType_table.format(type = 'EtherType', data = 'Value (numbers are in hex)', desc = 'desc'))
    printList.append(etherType_table_line)

    # Print if Tagged traffic
    if pkt_object.tagged == True:
        printList.append(etherType_table.format(type = '802.1Q', data = '8100', desc = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'VLAN ID: '+pkt_object.vlan_id.hex().upper().lstrip('0'), desc = ''))
        printList.append(etherType_table_line)

    # Print if ARP packet
    if pkt_object.ethertype.hex() == '0806':
        # Print ARP stuff
        printList.append(etherType_table.format(type = 'ARP', data = '0806', desc = pkt_object.ethertype_desc))
        printList.append(etherTypedata_table.format(type = '', data = 'Hardware Type: '+pkt_object.arp.hardware_type.hex().upper().lstrip('0'), desc = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Protocol Type: '+pkt_object.arp.protocol_type.hex().upper(), desc = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Hardware Size: '+pkt_object.arp.hardware_size.hex().upper().lstrip('0'), desc = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Protocol Size: '+pkt_object.arp.protocol_size.hex().upper().lstrip('0'), desc = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Opcode: '+pkt_object.arp.opcode.hex().upper().lstrip('0'), desc = ''))
        
        # ARP provides MAC address as well, is different when Opcode = 1 (request)
        printList.append(bar)
        print_address(type = '', data = 'MAC Address', desc='Vendor ID')
        print_address_line()
        print_address(type = 'ARP Sender', data = pkt_object.arp.sender_mac_address.hex(':').upper(), desc = '')
        print_address(type = 'ARP Target', data = pkt_object.arp.target_mac_address.hex(':').upper(), desc = '')
        print_address_line()

        # IP address
        print_address(type = '', data = 'IP Address', desc='Location')
        print_address_line()
        print_address(type = 'ARP Sender', data = bytes2ip.format(*pkt_object.arp.sender_ip_address), desc = '')
        print_address(type = 'ARP Target', data = bytes2ip.format(*pkt_object.arp.target_ip_address), desc = '')

    
        printList.append(bar)  


    return printList
    

def printPKTinfo(pkt_object):
    printList = createPrintList(pkt_object)

    #os.system('cls')
    
    for line in printList:
        print(line)

    hexdump.hexdump(pkt_object.packet)
    print('\n'*5)


