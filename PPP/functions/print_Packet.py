# Given a packet we want first parse the packet, but since the parsed 
# information will be used later, we want a seperate function to print that 
# information. 

# want to use this to contain a 'convenience' function that prints each set of 
# info - I really should have the entire tree in here

# tree:
# Ethernet
#   ARP
#   IPv4
#       ICMP
#       UDP
#           sFlow
#               flow_sample
#               counters_sample

from PPP.protocols import Ethernet, ARP, IPv4, ICMP, UDP
from PPP.protocols.sFlow import sFlow, flow_sample, counters_sample

def Printer(Packet):
    Parent = Ethernet.print_Ethernet(Packet)

    if Packet.ethertype.hex() == '0806':
        ARP.print_ARP(Parent)

    elif Packet.ethertype.hex() == '0800':
        IPv4.print_IPv4(Parent)
        IPv4_tree(Packet, Parent)
    
    Parent.pf.print_bar()

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
    if sFlow.samples[0:4].hex() == '00000001':
        flow_sample.print_flow_sample(Parent)
    elif sFlow.samples[0:4].hex() == '00000002':
        counters_sample.print_counters_sample(Parent)
        