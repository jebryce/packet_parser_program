import hexdump
import os
def printPKTinfo(pkt_dict):
    #os.system('cls')
    bar_length = 125
    # Print MAC address info
    pkt_table = "  {type:>11} | {dataType:^17} | {description}"
    etherType_table = "  {type:>11} | {dataName:^9} | {dataValue:^6} | {description}"
    print(bar_length*'%')
    print(pkt_table.format(type = '', dataType = 'MAC Address', description='Vendor ID'))
    print(14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-')
    print(pkt_table.format(type = 'Source', dataType = pkt_dict['Source MAC Adress'].hex(':').upper(), description = ''))
    print(pkt_table.format(type = 'Destination', dataType = pkt_dict['Destination MAC Adress'].hex(':').upper(), description = ''))

    # Print IPv4 address info
    print(bar_length*'%')
    print(pkt_table.format(type = '', dataType = 'IP Address', description='Location'))
    print(14*'-'+'+'+19*'-'+'+'+(bar_length-35)*'-')
    print(pkt_table.format(type = 'Source', dataType = pkt_dict['Source MAC Adress'].hex(':').upper(), description = ''))
    print(pkt_table.format(type = 'Destination', dataType = pkt_dict['Destination MAC Adress'].hex(':').upper(), description = ''))

    # Print EtherType info
    print(bar_length*'%')
    print(etherType_table.format(type = '', dataName = 'Name', dataValue='Value', description = 'Description'))
    print(14*'-'+'+'+11*'-'+'+'+8*'-'+'+'+(bar_length-35)*'-')
    for etherType in pkt_dict['EtherTypes']:
        print(etherType_table.format(type = pkt_dict['EtherTypes'][etherType][0], dataName = etherType, dataValue = pkt_dict['EtherTypes'][etherType][1].hex(), description = ''))



    print('\n'*3)
    hexdump.hexdump(pkt_dict['Raw Data'])