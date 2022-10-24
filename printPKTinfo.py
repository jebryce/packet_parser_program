import hexdump
import os
def createPrintList(pkt_object):
    
    # bar_length is the number of characters wide to print the table row borders
    bar_length = 125
    
    # This function populates a list full of strings
    printList = []


    # Initialize string formats
    bar = bar_length*'%'
    pkt_table = "  {type:>11} | {dataType:^17} | {description}"
    pkt_table_line = 14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-'
    etherType_table_line = 14*'-'+'+'+32*'-'+'+'+(bar_length-48)*'-'
    etherType_table = "  {type:>11} | {data:<30} | {description}"
    etherTypedata_table = "  {type:>11} |--> {data:<27} | {description}"


    # Honestly am surprised this worked
    bytes2ip = '{}.{}.{}.{}'
    # example: bytes2ip.format(*variable)
    # need the asterisk



    # Print MAC address info
    printList.append(bar)
    printList.append(pkt_table.format(type = '', dataType = 'MAC Address', description='Vendor ID'))
    printList.append(pkt_table_line)
    printList.append(pkt_table.format(type = 'Source', dataType = pkt_object.source_mac_address.hex(':').upper(), description = ''))
    printList.append(pkt_table.format(type = 'Destination', dataType = pkt_object.destination_mac_address.hex(':').upper(), description = ''))

    
    # Print EtherType info
    printList.append(bar)
    printList.append(etherType_table.format(type = 'EtherType', data = 'Value (numbers are in hex)', description = 'Description'))
    printList.append(etherType_table_line)

    # Print if Tagged traffic
    if pkt_object.tagged == True:
        printList.append(etherType_table.format(type = '802.1Q', data = '8100', description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'VLAN ID: '+pkt_object.vlan_id.hex().upper().lstrip('0'), description = ''))
        printList.append(etherType_table_line)

    # Print if ARP packet
    if pkt_object.ethertype.hex() == '0806':
        # Print ARP stuff
        printList.append(etherType_table.format(type = 'ARP', data = '0806', description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Hardware Type: '+pkt_object.arp.hardware_type.hex().upper().lstrip('0'), description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Protocol Type: '+pkt_object.arp.protocol_type.hex().upper(), description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Hardware Size: '+pkt_object.arp.hardware_size.hex().upper().lstrip('0'), description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Protocol Size: '+pkt_object.arp.protocol_size.hex().upper().lstrip('0'), description = ''))
        printList.append(etherTypedata_table.format(type = '', data = 'Opcode: '+pkt_object.arp.opcode.hex().upper().lstrip('0'), description = ''))
        
        # ARP provides MAC address as well, is different when Opcode = 1 (request)
        printList.append(bar)
        printList.append(pkt_table.format(type = '', dataType = 'MAC Address', description='Vendor ID'))
        printList.append(pkt_table_line)
        printList.append(pkt_table.format(type = 'ARP Sender', dataType = pkt_object.arp.sender_mac_address.hex(':').upper(), description = ''))
        printList.append(pkt_table.format(type = 'ARP Target', dataType = pkt_object.arp.target_mac_address.hex(':').upper(), description = ''))
        printList.append(pkt_table_line)

        # IP address
        printList.append(pkt_table.format(type = '', dataType = 'IP Address', description='Vendor ID'))
        printList.append(pkt_table_line)
        printList.append(pkt_table.format(type = 'ARP Sender', dataType = bytes2ip.format(*pkt_object.arp.sender_ip_address), description = ''))
        printList.append(pkt_table.format(type = 'ARP Target', dataType = bytes2ip.format(*pkt_object.arp.target_ip_address), description = ''))


    
            
    printList.append('\n'*2)
    return printList
    

def printPKTinfo(pkt_object):
    printList = createPrintList(pkt_object)

    os.system('cls')
    
    for line in printList:
        print(line)

    hexdump.hexdump(pkt_object.packet)


