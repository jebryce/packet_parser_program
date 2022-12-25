# Given a packet with type 'bytes', we want to be able to fully parse the 
# packet down to what every byte does. 
#
# 
#
# A way to call the class's variables, for example:
# my_Packet = Packet(bytes), where bytes is a packet of type bytes
# my_Packet.ethertype                  | returns a bytes object
#                                      | ex: 0806 (type: bytes)
# my_Packet.desc.ethertype             | returns a string that describes
#                                      | ex: 'Address Resolution Protocol (ARP)'
# my_Packet.ARP.opcode                 | returns a bytes object
#                                      | ex: 01 (type: bytes)
# my_Packet.ARP.desc.opcode            | returns a string that describes
#                                      | ex: 'Request' (type: string)
# generally:                           |
# my_Packet.variable                   | calls the data of variable
# my_Packet.desc.variable              | calls the description of variable
# 
from PPP.protocols import Ethernet, ARP, IPv4, ICMP, UDP
from PPP.protocols.sFlow import sFlow, flow_sample, counters_sample, raw_packet_header, extended_switch_data

# create both parsed data and the descriptions

# tree:
# Ethernet
#   ARP
#   IPv4
#       ICMP
#       UDP
#           sFlow
#               flow_sample
#               counters_sample


def Parser(packet):
    Packet = Ethernet.Ethernet(packet)
    Packet.desc = Ethernet.Ethernet_desc(Packet)

    if Packet.ethertype.hex() == '0806':
        Packet.ARP = ARP.ARP(Packet)
        Packet.ARP.desc = ARP.ARP_desc(Packet)

    elif Packet.ethertype.hex() == '0800':
        Packet.IPv4 = IPv4.IPv4(Packet)
        Packet.IPv4.desc = IPv4.IPv4_desc(Packet)
        IPv4_tree(Packet)

    Packet.desc.finish_descriptions(Packet)
    return Packet

def IPv4_tree(Packet):
    if Packet.IPv4.protocol.hex() == '01':
        Packet.IPv4.ICMP = ICMP.ICMP(Packet)
        Packet.IPv4.ICMP.desc = ICMP.ICMP_desc(Packet)

    # 11 hex = 17 dec
    elif Packet.IPv4.protocol.hex() == '11':
        Packet.IPv4.UDP = UDP.UDP(Packet)
        Packet.IPv4.UDP.desc = UDP.UDP_desc(Packet)
        UDP_tree(Packet)

def UDP_tree(Packet):
    # 18c7 hex = 6343 dec
    if Packet.IPv4.UDP.destination_port.hex() == '18c7':
        Packet.IPv4.UDP.sFlow = sFlow.sFlow(Packet)
        Packet.IPv4.UDP.sFlow.desc = sFlow.sFlow_desc(Packet)
        sFlow_tree(Packet)

def sFlow_tree(Packet):
    sFlow = Packet.IPv4.UDP.sFlow

    for sample in range(int.from_bytes(sFlow.number_of_samples,'big')):
        if sFlow.samples[0:4].hex() == '00000001':
            sFlow.flow_sample = flow_sample.flow_sample(Packet)
            sFlow.flow_sample.desc = flow_sample.flow_sample_desc(Packet)
            
            sFlow.flow_sample.raw_packet_header = \
                raw_packet_header.raw_packet_header(Packet)
            sFlow.flow_sample.raw_packet_header.desc = \
                raw_packet_header.raw_packet_header_desc(Packet)

            sFlow.flow_sample.extended_switch_data = \
                extended_switch_data.extended_switch_data(Packet)
            sFlow.flow_sample.extended_switch_data.desc = \
                extended_switch_data.extended_switch_data_desc(Packet)

            raw_header = sFlow.flow_sample.raw_packet_header
            raw_header.Packet = Parser(raw_header.sampled_packet)

            # the sample_length value seems to be 8 less than usual
            # I am assuming sFlow does not count the 4 enterprise/format bytes 
            # and the 4 sample_length bytes as part of the sample_length
            index = int.from_bytes(sFlow.flow_sample.sample_length, 'big') + 8

            sFlow.samples = sFlow.samples[index:]


        elif sFlow.samples[0:4].hex() == '00000002':
            sFlow.counters_sample = counters_sample.counters_sample(Packet)
            sFlow.counters_sample.desc = \
                counters_sample.counters_sample_desc(Packet)
            
            # the sample_length value seems to be 8 less than usual
            # I am assuming sFlow does not count the 4 enterprise/format bytes 
            # and the 4 sample_length bytes as part of the sample_length
            index = \
                int.from_bytes(sFlow.counters_sample.sample_length, 'big') + 8
            sFlow.samples = sFlow.samples[index:]
            
            
        