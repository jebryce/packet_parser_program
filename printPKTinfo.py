import hexdump
import os
def printPKTinfo(pkt_dict):
    #os.system('cls')
    bar_length = 125
    # Print MAC address info
    pkt_table = "  {type:>11} | {dataType:^17} | {description}"
    etherType_table = "  {type:>11} | {dataType:^4} | {value:^10} | {description}"
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
    print(etherType_table.format(type = 'EtherType', dataType = 'Hex', value='VLAN ID',description = 'Description'))
    print(14*'-'+'+'+6*'-'+'+'+12*'-'+'+'+(bar_length-35)*'-')
    print(etherType_table.format(type = '802.1Q', dataType = pkt_dict['VLAN EtherType'].hex().upper(), value = pkt_dict['VLAN ID'].hex().upper(), description = ''))



    print('\n'*3)
    hexdump.hexdump(pkt_dict['Raw Data'])