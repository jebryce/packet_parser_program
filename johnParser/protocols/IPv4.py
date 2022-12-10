from johnParser.protocols import Ethernet

class IPv4():
    def __init__(self, Packet):

        Packet.update_widths(8, 23)

        self.version = (Packet.partial_packet[0] >> 4).to_bytes(1,'big')
        self.ihl = (Packet.partial_packet[0] & 0b1111).to_bytes(1,'big')
        self.dscp = (Packet.partial_packet[1] >> 2).to_bytes(2,'big')
        self.ecn = (Packet.partial_packet[1] & 0b11).to_bytes(1,'big')

        self.total_length = Packet.partial_packet[2:4]
        self.identification = Packet.partial_packet[4:6]

        self.flags = (Packet.partial_packet[6] >> 5).to_bytes(1,'big')

        self.fragment_offset = Packet.partial_packet[6] & 0b11111 * 256
        self.fragment_offset += Packet.partial_packet[7]
        self.fragment_offset = self.fragment_offset.to_bytes(1,'big')



        self.ttl = Packet.partial_packet[8:9]
        self.protocol = Packet.partial_packet[9:10]
        self.checksum = Packet.partial_packet[10:12]
        self.source_ip_address = Packet.partial_packet[12:16]
        self.destination_ip_address = Packet.partial_packet[16:20]

        self.partial_packet = Packet.partial_packet[20:]

class IPv4_desc():
    def __init__(self, Packet):
        self.version ='Version of the IP protocol. Should always be 4 for IPv4.'
        self.ihl = 'Length of the IPv4 header in number of 32-bit words. Minimum 5.'
        self.dscp = 'Differentiated Services Code Point. Default 0.'
        self.ecn = 'Explicit Congestion Notification. Is an optional feature.'
        self.total_length = 'Length of the entire packet, from this IPv4 header onwards.'
        self.identification = 'Used for identifying a group of fragments.'
        self.flags = 'Used to control or identify fragments.'
        self.fragment_offset = 'Used to specify the offset of a particular fragment.'
        self.ttl = 'Specified in seconds, but is used in practice as a hop count.'
        self.protocol = 'Placeholder for IPv4 protocol lookup.'
        self.checksum = 'Used for error checking of the IPv4 header.'

        # TODO implement ip address lookup
        self.source_ip_address = 'Placeholder for IPv4 address lookup.'
        self.destination_ip_address = 'Placeholder for IPv4 address lookup.'

class print_IPv4(Ethernet.print_Ethernet):
    def __init__(self, parent):
        parent.print_ipv4_address_table(
            'Source',
            parent.Packet.IPv4.source_ip_address,
            parent.Packet.IPv4.desc.source_ip_address,
            'Destination',
            parent.Packet.IPv4.destination_ip_address,
            parent.Packet.IPv4.desc.destination_ip_address
        )

        parent.print_ethertype('IPv4')

        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Version',
                parent.Packet.IPv4.version.hex().upper(), 
                parent.Packet.IPv4.desc.version
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Header Length',
                parent.Packet.IPv4.ihl.hex().upper(), 
                parent.Packet.IPv4.desc.ihl
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'DSCP',
                parent.Packet.IPv4.dscp.hex().upper(), 
                parent.Packet.IPv4.desc.dscp
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'ECN',
                parent.Packet.IPv4.ecn.hex().upper(), 
                parent.Packet.IPv4.desc.ecn
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Total Length',
                parent.Packet.IPv4.total_length.hex().upper(), 
                parent.Packet.IPv4.desc.total_length
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Identification',
                parent.Packet.IPv4.identification.hex().upper(), 
                parent.Packet.IPv4.desc.identification
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Flags',
                parent.Packet.IPv4.flags.hex().upper(), 
                parent.Packet.IPv4.desc.flags
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Fragment Offset',
                parent.Packet.IPv4.fragment_offset.hex().upper(), 
                parent.Packet.IPv4.desc.fragment_offset
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Time to Live',
                parent.Packet.IPv4.ttl.hex().upper(), 
                parent.Packet.IPv4.desc.ttl
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Protocol',
                parent.Packet.IPv4.protocol.hex().upper(), 
                parent.Packet.IPv4.desc.protocol
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.checksum.hex().upper(), 
                parent.Packet.IPv4.desc.checksum
            ],
            arrow_length = 3
        )
