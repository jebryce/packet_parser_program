# Given a packet we want first parse the packet, but since the parsed 
# information will be used later, we want a seperate function to print that 
# information. 
#
# want to use this to contain a 'convenience' function that prints each set of 
# info - I really should have the entire tree in here
#
# tree:
# Ethernet
#   ARP
#   IPv4
#       ICMP
#       UDP
#           sFlow
#               flow_sample
#                   raw_packet_header
#                       (recurses back to start of tree)
#                   extended_switch_data
#               counters_sample

from PPP.protocols import Ethernet, ARP, IPv4, ICMP, UDP
from PPP.protocols.sFlow import sFlow, flow_sample, counters_sample, raw_packet_header, extended_switch_data

def Printer(Packet):
    Parent = Ethernet.print_Ethernet(Packet)

    if Packet.ethertype.hex() == '0806':
        ARP.print_ARP(Parent)

    elif Packet.ethertype.hex() == '0800':
        IPv4.print_IPv4(Parent)
        IPv4_tree(Packet, Parent)
    
   

def IPv4_tree(Packet, Parent):
    if Packet.IPv4.protocol.hex() == '01':
        ICMP.print_ICMP(Parent)

    # 11 hex = 17 dec
    elif Packet.IPv4.protocol.hex() == '11':
        UDP.print_UDP(Parent)
        UDP_tree(Packet, Parent)

def UDP_tree(Packet, Parent):
    # 18c7 hex = 6343 dec
    if Packet.IPv4.UDP.destination_port.hex() == '18c7':
        sFlow.print_sFlow(Parent)
        sFlow_tree(Packet, Parent)

def sFlow_tree(Packet, Parent):
    sFlow = Packet.IPv4.UDP.sFlow
    index = 0
    for sample in range(int.from_bytes(sFlow.number_of_samples,'big')):
        if sFlow.samples[index:index + 4].hex() == '00000001':
            flow_sample.print_flow_sample(Parent, sample)
            raw_packet_header.print_raw_packet_header(Parent)
            extended_switch_data.print_extended_switch_data(Parent)
            # recurses back to the start of the tree
            # Printer(sFlow.flow_sample.raw_packet_header.Packet)
            index += \
                int.from_bytes(sFlow.flow_sample.sample_length, 'big') + 8

        elif sFlow.samples[index:index + 4].hex() == '00000002':
            counters_sample.print_counters_sample(Parent, sample)
            index += \
                int.from_bytes(sFlow.counters_sample.sample_length, 'big') + 8
        