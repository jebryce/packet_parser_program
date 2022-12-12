from PPP.protocols import Ethernet
class UDP():
    def __init__(self, Packet):

        Packet.update_widths(8, 25)

        self.source_port = Packet.IPv4.partial_packet[0:2]
        self.destination_port = Packet.IPv4.partial_packet[2:4]
        self.length = Packet.IPv4.partial_packet[4:6]
        self.checksum = Packet.IPv4.partial_packet[6:8]
        self.payload = Packet.IPv4.partial_packet[8:]

class UDP_desc():
    def __init__(self, Packet):
        self.source_port = 'Placeholder for UDP port lookup.'
        self.destination_port = 'Placeholder for UDP port lookup.'
        self.length = 'Length of the UDP header and data.'
        self.checksum = 'May be used for error checking of the UDP header and data.'

class print_UDP(Ethernet.print_Ethernet):
    def __init__(self, parent):
        parent.pf.print_data_bar(parent.widths)
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'UDP',
                '11', 
                'User Datagram Protocol'
            ]
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Source Port',
                parent.Packet.IPv4.UDP.source_port.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.source_port
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Destination Port',
                parent.Packet.IPv4.UDP.destination_port.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.destination_port
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Length',
                parent.Packet.IPv4.UDP.length.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.length
            ],
            arrow_length = 3
        )
        parent.pf.print_data( 
            column_widths = parent.widths,
            entries = [
                'Checksum',
                parent.Packet.IPv4.UDP.checksum.hex().upper(), 
                parent.Packet.IPv4.UDP.desc.checksum
            ],
            arrow_length = 3
        )
