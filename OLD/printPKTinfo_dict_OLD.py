import hexdump
import os
def createPrintList(pkt_dict):
    bar_length = 125
    printList = []


    # Print MAC address info
    pkt_table = "  {type:>11} | {dataType:^17} | {description}"
    etherType_table = "  {type:>11} | {data:<30} | {description}"
    etherTypedata_table = "  {type:>11} |--> {data:<27} | {description}"
    printList.append(bar_length*'%')
    printList.append(pkt_table.format(type = '', dataType = 'MAC Address', description='Vendor ID'))
    printList.append(14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-')
    printList.append(pkt_table.format(type = 'Source', dataType = pkt_dict['Source MAC Adress'].hex(':').upper(), description = ''))
    printList.append(pkt_table.format(type = 'Destination', dataType = pkt_dict['Destination MAC Adress'].hex(':').upper(), description = ''))

    # Print IPv4 address info
    printList.append(bar_length*'%')
    printList.append(pkt_table.format(type = '', dataType = 'IP Address', description='Location'))
    printList.append(14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-')
    printList.append(pkt_table.format(type = 'Source', dataType = pkt_dict['Source MAC Adress'].hex(':').upper(), description = ''))
    printList.append(pkt_table.format(type = 'Destination', dataType = pkt_dict['Destination MAC Adress'].hex(':').upper(), description = ''))

    # Print EtherType info
    printList.append(bar_length*'%')
    printList.append(etherType_table.format(type = 'EtherType', data = 'Value (numbers in hex)', description = 'Description'))
    for etherType in pkt_dict['EtherTypes']:
        printList.append(14*'-'+'+'+32*'-'+'+'+(bar_length-48)*'-')
        printList.append(etherType_table.format(type = etherType, data = pkt_dict['EtherTypes'][etherType].hex().upper(), description = ''))
        if etherType == '802.1Q':
            printList.append(etherTypedata_table.format(type = '', data = 'VLAN ID: '+pkt_dict['VLAN ID'].hex().upper().lstrip('0'), description = ''))
        elif etherType == 'ARP':
            printList.append(etherTypedata_table.format(type = '', data = 'Hardware Type: '+pkt_dict['ARP Hardware Type'].hex().upper().lstrip('0'), description = ''))
        
            
    printList.append('\n'*2)
    return printList
    

def printPKTinfo(pkt_dict):
    printList = createPrintList(pkt_dict)

    os.system('cls')
    
    for line in printList:
        print(line)

    hexdump.hexdump(pkt_dict['Raw Data'])


